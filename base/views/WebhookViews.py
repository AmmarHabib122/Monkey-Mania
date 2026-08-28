import hashlib
import hmac
import ipaddress
import json
import time

from django.conf import settings
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from base import models, services




SENSITIVE_HEADERS = {'authorization', 'cookie', 'proxy-authorization', 'set-cookie'}
SENSITIVE_QUERY_PARAMS = {'hub.verify_token'}


def _request_headers(request):
    return {
        name: '[REDACTED]' if name.lower() in SENSITIVE_HEADERS else value
        for name, value in request.headers.items()
    }


def _request_query_params(request):
    return {
        name: '[REDACTED]' if name.lower() in SENSITIVE_QUERY_PARAMS else value
        for name, value in request.query_params.items()
    }


def _client_ip(request):
    possible_ips = (
        request.META.get('HTTP_CF_CONNECTING_IP'),
        (request.META.get('HTTP_X_FORWARDED_FOR') or '').split(',')[0].strip(),
        request.META.get('REMOTE_ADDR'),
    )
    for value in possible_ips:
        try:
            return str(ipaddress.ip_address(value))
        except (TypeError, ValueError):
            continue
    return None


def _record_webhook_call(
    request,
    started_at,
    event_type,
    is_valid,
    response_status,
    processing_result,
    payload=None,
    raw_body='',
):
    try:
        models.WebhookCall.objects.create(
            route=request.path,
            method=request.method,
            event_type=event_type,
            payload=payload,
            raw_body=raw_body,
            headers=_request_headers(request),
            query_params=_request_query_params(request),
            ip_address=_client_ip(request),
            is_valid=is_valid,
            response_status=response_status,
            processing_result=processing_result,
            duration_ms=max(int((time.monotonic() - started_at) * 1000), 0),
        )
    except Exception:
        # Webhook logging must never prevent Meta from receiving a response.
        pass


def _parse_payload(body):
    raw_body = body.decode('utf-8', errors='replace')
    if not body:
        return None, raw_body, 'Request body is empty'
    try:
        return json.loads(raw_body), '', None
    except json.JSONDecodeError as exc:
        return None, raw_body, str(exc)


def _has_valid_signature(body, signature):
    expected_signature = 'sha256=' + hmac.new(
        settings.WHATSAPP_APP_SECRET.encode('utf-8'),
        body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)


class WhatsAppStatusWebhookAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        """Complete Meta's callback URL verification challenge."""
        started_at = time.monotonic()
        challenge = request.query_params.get('hub.challenge')
        is_valid = (
            bool(settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN)
            and request.query_params.get('hub.mode') == 'subscribe'
            and request.query_params.get('hub.verify_token')
            == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN
            and challenge is not None
        )

        if is_valid:
            response_status = 200
            result = {'verified': True}
            response = HttpResponse(challenge, content_type='text/plain')
        else:
            response_status = 503 if not settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN else 403
            result = {'reason': 'invalid_verification_request'}
            response = HttpResponse(status=response_status)

        _record_webhook_call(
            request,
            started_at,
            'verification',
            is_valid,
            response_status,
            result,
        )
        return response

    def post(self, request):
        """Validate and process a WhatsApp status callback from Meta."""
        started_at = time.monotonic()
        body = request.body
        payload, raw_body, payload_error = _parse_payload(body)
        is_valid = False
        response_status = 500
        result = {}

        try:
            if not settings.WHATSAPP_APP_SECRET:
                response_status = 503
                result = {'reason': 'whatsapp_app_secret_not_configured'}
            elif not _has_valid_signature(
                body,
                request.headers.get('X-Hub-Signature-256', ''),
            ):
                response_status = 403
                result = {'reason': 'invalid_signature'}
            elif payload_error:
                response_status = 400
                result = {'reason': 'invalid_json', 'error': payload_error[:1000]}
            else:
                try:
                    updated_messages = services.process_whatsapp_status_webhook(payload)
                except services.InvalidWhatsAppWebhookPayload as exc:
                    response_status = 400
                    result = {'reason': 'invalid_payload', 'error': str(exc)}
                else:
                    is_valid = True
                    response_status = 200
                    result = {'updated_messages': updated_messages}

            return HttpResponse(status=response_status)
        except Exception as exc:
            result = {
                'reason': 'unexpected_error',
                'error_type': type(exc).__name__,
                'error': str(exc)[:1000],
            }
            raise
        finally:
            _record_webhook_call(
                request,
                started_at,
                'whatsapp_status_callback',
                is_valid,
                response_status,
                result,
                payload,
                raw_body,
            )


Update_WhatsappMessageStatus = WhatsAppStatusWebhookAPI.as_view()

import re

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from base import models


RELATIONSHIP_PRIORITY = ('mother', 'father', 'sibling')


def normalize_phone_number(phone_number):
    """Convert a stored local phone number to WhatsApp's international digits format."""
    digits = re.sub(r'\D', '', str(phone_number or ''))
    if digits.startswith('00'):
        digits = digits[2:]
    elif digits.startswith('0'):
        digits = f"{settings.WHATSAPP_DEFAULT_COUNTRY_CODE}{digits[1:]}"
    return digits


def select_child_phone_number(child):
    phone_links = sorted(
        child.child_phone_numbers_set.all(),
        key=lambda phone_link: phone_link.pk,
    )
    if not phone_links:
        return None

    for relationship in RELATIONSHIP_PRIORITY:
        for phone_link in phone_links:
            if phone_link.relationship.strip().lower() == relationship:
                return phone_link.phone_number.value
    return phone_links[0].phone_number.value


def _format_finished_date(bill):
    finished = timezone.localtime(bill.finished or timezone.now())
    return finished.strftime('%b %d, %Y').replace(' 0', ' ')


def _build_payload(bill, phone_number, child_names):
    return {
        'messaging_product': 'whatsapp',
        'to': phone_number,
        'type': 'template',
        'template': {
            'name': settings.WHATSAPP_TEMPLATE_NAME,
            'language': {'code': settings.WHATSAPP_TEMPLATE_LANGUAGE},
            'components': [
                {
                    'type': 'body',
                    'parameters': [
                        {'type': 'text', 'text': ', '.join(child_names)},
                        {'type': 'text', 'text': bill.serial or str(bill.pk)},
                        {'type': 'text', 'text': _format_finished_date(bill)},
                    ],
                },
            ],
        },
    }


def _reserve_recipients(bill):
    """Create one message record per unique selected phone number in the bill."""
    with transaction.atomic():
        children = bill.children.prefetch_related(
            'child_phone_numbers_set__phone_number',
        ).order_by('id')
        existing_phone_numbers = set(
            bill.whatsapp_messages.values_list('phone_number', flat=True)
        )
        phone_groups = {}

        for child in children:
            selected_phone = select_child_phone_number(child)
            normalized_phone = normalize_phone_number(selected_phone)
            if not normalized_phone or normalized_phone in existing_phone_numbers:
                continue

            if normalized_phone in phone_groups:
                phone_groups[normalized_phone]['child_names'].append(child.name)
                continue

            recipient = models.WhatsAppMessage.objects.create(
                bill=bill,
                child=child,
                phone_number=normalized_phone,
            )
            phone_groups[normalized_phone] = {
                'message': recipient,
                'child_names': [child.name],
            }

        return phone_groups


def _update_message(
    message,
    log_entry,
    status=None,
    provider_message_id=None,
):
    now = timezone.now()
    log = {
        **log_entry,
        'timestamp': now.isoformat(),
    }
    update_fields = ['logs', 'updated']

    if status is not None:
        update_fields.append('status')
    if provider_message_id is not None:
        update_fields.append('provider_message_id')

    message.logs = [*message.logs, log]
    if status is not None:
        message.status = status
    if provider_message_id is not None:
        message.provider_message_id = provider_message_id
    message.updated = now
    message.save(update_fields=update_fields)


def send_bill_experience_messages(bill):
    """Send one template message per unique preferred number after an eligible close."""
    if not settings.WHATSAPP_MESSAGES_ENABLED:
        return 0
    if bill.is_active or bill.spent_time < settings.WHATSAPP_MIN_BILL_MINUTES:
        return 0
    if not all((
        settings.WHATSAPP_ACCESS_TOKEN,
        settings.WHATSAPP_PHONE_NUMBER_ID,
        settings.WHATSAPP_TEMPLATE_NAME,
    )):
        return 0

    try:
        phone_groups = _reserve_recipients(bill)
    except Exception:
        return 0

    endpoint = (
        f"https://graph.facebook.com/{settings.WHATSAPP_GRAPH_API_VERSION}/"
        f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    )
    headers = {
        'Authorization': f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        'Content-Type': 'application/json',
    }
    sent_count = 0

    for phone_number, phone_group in phone_groups.items():
        message = phone_group['message']
        child_names = phone_group['child_names']
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=_build_payload(bill, phone_number, child_names),
                timeout=settings.WHATSAPP_REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            response_data = response.json()
            provider_message_id = (response_data.get('messages') or [{}])[0].get('id')
            if not provider_message_id:
                raise ValueError('Meta response does not contain a message ID')
            _update_message(
                message,
                {
                    'event': 'api_success',
                    'response': response_data,
                },
                status=models.WhatsAppMessage.Status.SENT,
                provider_message_id=provider_message_id,
            )
            sent_count += 1
        except (
            requests.RequestException,
            ValueError,
            TypeError,
            AttributeError,
            KeyError,
            IndexError,
        ) as exc:
            error_text = str(exc)[:1000]
            _update_message(
                message,
                {
                    'event': 'api_error',
                    'error': error_text,
                },
            )

    return sent_count

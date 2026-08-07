from django.db import models


class WebhookCall(models.Model):
    route = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField(null=True, blank=True)
    raw_body = models.TextField(blank=True, default='')
    headers = models.JSONField(default=dict, blank=True)
    query_params = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    response_status = models.PositiveSmallIntegerField(null=True, blank=True)
    processing_result = models.JSONField(default=dict, blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'webhook_calls'
        ordering = ['-created']

    def __str__(self):
        return f"{self.method} {self.route} - {self.response_status}"

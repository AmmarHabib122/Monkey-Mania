from django.db import models


class WhatsAppMessage(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        READ = 'read', 'Read'
        FAILED = 'failed', 'Failed'
        DELETED = 'deleted', 'Deleted'

    bill = models.ForeignKey(
        'base.Bill',
        on_delete=models.CASCADE,
        related_name='whatsapp_messages',
    )
    child = models.ForeignKey(
        'base.Child',
        on_delete=models.CASCADE,
        related_name='bill_whatsapp_messages',
    )
    phone_number = models.CharField(max_length=20, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    provider_message_id = models.CharField(max_length=255, null=True, blank=True)
    sent_by = models.ForeignKey(
        'base.User',
        on_delete=models.SET_NULL,
        related_name='sent_whatsapp_messages',
        null=True,
        blank=True,
    )
    logs = models.JSONField(default=list, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bill', 'phone_number'],
                name='unique_whatsapp_message_per_bill_phone',
            ),
        ]

    def __str__(self):
        return f"Bill #{self.bill_id} - Child #{self.child_id} - {self.status} -  {self.phone_number}"

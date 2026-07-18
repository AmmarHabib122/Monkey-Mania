import datetime

from django.db import models
from django.utils import timezone


class BillTimePause(models.Model):
    bill = models.ForeignKey(
        'base.Bill',
        on_delete=models.CASCADE,
        related_name='pauses',
    )
    reason = models.TextField()
    finished = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'base.User',
        on_delete=models.PROTECT,
        related_name='created_bill_time_pauses_set',
    )
    finished_by = models.ForeignKey(
        'base.User',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='finished_bill_time_pauses_set',
    )

    @property
    def is_active(self):
        return self.finished is None

    @property
    def duration_in_seconds(self):
        end = self.finished or timezone.now()
        return max(end - self.created, datetime.timedelta(0)).total_seconds()

    def __str__(self):
        return f"Pause #{self.id} for bill #{self.bill_id} for {self.duration_in_seconds / 60:.2f} minutes "

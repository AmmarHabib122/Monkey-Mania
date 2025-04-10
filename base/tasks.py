from celery import shared_task

from base import models




@shared_task
def create_daily_income_task():
    ...
    # DailyIncome.objects.create()
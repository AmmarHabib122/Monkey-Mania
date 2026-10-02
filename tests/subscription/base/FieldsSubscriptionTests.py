from django.urls import reverse
from rest_framework import status

from base import models
from .SetUpSubscriptionTests import SetUpDataClass


class TestSubscriptionFields(SetUpDataClass):
    def test_hours_use_half_hour_increments(self):
        self.authenticate(self.admin_user_1)
        payload = {**self.test_subscription_1, 'hours': 1.25}
        response = self.client.post(reverse('Create_Subscription'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(models.Subscription.objects.filter(name='testsubscription1').exists())

    def test_duration_is_at_least_seven_days(self):
        self.authenticate(self.admin_user_1)
        payload = {**self.test_subscription_1, 'instance_duration': 6}
        response = self.client.post(reverse('Create_Subscription'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

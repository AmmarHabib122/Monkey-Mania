from django.urls import reverse
from rest_framework import status

from base import models
from .SetUpSubscriptionInstanceTests import SetUpDataClass


class TestSubscriptionInstanceFields(SetUpDataClass):
    def test_new_instance_uses_subscription_hours(self):
        self.authenticate(self.admin_user_1)
        response = self.client.post(reverse('Create_SubscriptionInstance'), self.test_subscription_instance_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        instance = models.SubscriptionInstance.objects.get(pk=response.data['id'])
        self.assertEqual(instance.base_hours, self.subscription_1.hours)
        self.assertEqual(instance.remaining_hours, self.subscription_1.hours)

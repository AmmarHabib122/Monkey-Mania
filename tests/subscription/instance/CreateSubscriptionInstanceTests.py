from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpSubscriptionInstanceTests import SetUpDataClass









class TestSubscriptionInstanceCreation(SetUpDataClass):
    def test_user_with_no_branch_create_subscription_instance(self):
        url = reverse('Create_SubscriptionInstance')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_subscription_instance_1, format = 'json') #admin add subscription_instance
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_subscription_instance(self):
        url = reverse('Create_SubscriptionInstance')
        self.authenticate(self.reception_user_1)
        
        response = self.client.post(url, self.test_subscription_instance_1, format = 'json') #recerption add subscription_instance
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_or_no_permission_create_subscription_instance(self):
        url = reverse('Create_SubscriptionInstance')
        self.authenticate(self.waiter_user_1)
        
        response = self.client.post(url, self.test_subscription_instance_1, format = 'json') #waiter add subscription_instance
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














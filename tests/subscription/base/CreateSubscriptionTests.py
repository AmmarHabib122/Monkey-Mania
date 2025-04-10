from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpSubscriptionTests import SetUpDataClass









class TestSubscriptionCreation(SetUpDataClass):
    def test_user_with_no_branch_create_subscription(self):
        url = reverse('Create_Subscription')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_subscription_1, format = 'json') #admin add subscription
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)







    def test_user_with_a_branch_or_no_permission_create_subscription(self):
        url = reverse('Create_Subscription')
        self.authenticate(self.manager_user_1)
        
        response = self.client.post(url, self.test_subscription_1, format = 'json') #waiter add subscription
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














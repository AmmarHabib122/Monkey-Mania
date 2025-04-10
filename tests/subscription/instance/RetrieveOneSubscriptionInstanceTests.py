from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpSubscriptionInstanceTests import SetUpDataClass





class TestSubscriptionInstanceRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_subscription_instance(self):
        self.authenticate(self.admin_user_1)

        url = reverse('Get_SubscriptionInstance', kwargs={'pk': 1})  #admin get SubscriptionInstance
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    

    def test_user_with_a_branch_get_subscription_instance(self):

        self.authenticate(self.reception_user_1)
        url = reverse('Get_SubscriptionInstance', kwargs={'pk': 1})  #manager get  SubscriptionInstance
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        




    def test_user_with_no_permission_get_subscription_instance(self):
        self.authenticate(self.waiter_user_1)
        
        url = reverse('Get_SubscriptionInstance', kwargs={'pk': 1})  #waiter get subscription_instance
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpSubscriptionTests import SetUpDataClass





class TestSubscriptionRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_subscription(self):
        self.authenticate(self.admin_user_1)

        url = reverse('Get_Subscription', kwargs={'pk': 1})  #admin get Subscription
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    

    def test_user_with_a_branch_get_subscription(self):

        self.authenticate(self.manager_user_1)
        url = reverse('Get_Subscription', kwargs={'pk': 1})  #manager get  Subscription
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        




    def test_user_with_no_permission_get_subscription(self):
        self.authenticate(self.reception_user_1)
        
        url = reverse('Get_Subscription', kwargs={'pk': 1})  #waiter get subscription
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpSubscriptionTests import SetUpDataClass





class TestSubscriptionUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_subscription(self):
        self.authenticate(user = self.admin_user_1)
        
        url = reverse('Update_Subscription', kwargs = {'pk' : 2})
        response = self.client.patch(url, self.test_subscription_1, format = 'json') #admin update Branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)






  

        


    def test_user_with_no_permission_update_subscription(self):
        self.authenticate(user = self.manager_user_1)
        
        url = reverse('Update_Subscription', kwargs = {'pk' : 2})
        response = self.client.patch(url, self.test_subscription_1, format = 'json') #waiter update Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    
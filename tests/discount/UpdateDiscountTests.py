from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpDiscountTests import SetUpDataClass





class TestDiscountUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_discount(self):
        url = reverse('Update_Discount', kwargs = {'pk' : 1})
        self.authenticate(user = self.admin_user_1)
        
        data = {
            'value' : '0.90'
        }
        response = self.client.patch(url, data, format = 'json') #admin update Discount
        self.assertEqual(response.status_code, status.HTTP_200_OK)






        


    def test_user_with_no_permission_update_discount(self):
        url = reverse('Update_Discount', kwargs = {'pk' : 1})
        self.authenticate(user = self.manager_user_1)

        data = {
            'value' : '90'
        }
        response = self.client.patch(url, data, format = 'json') #waiter update Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    
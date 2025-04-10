from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpDiscountTests import SetUpDataClass





class TestDiscountRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_discount(self):
        url = reverse('Get_Discount', kwargs={'pk': 1})
        self.authenticate(self.admin_user_1)

        response = self.client.get(url)                     #admin get Discount
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_a_branch_get_discount(self):
        url = reverse('Get_Discount', kwargs={'pk': 1}) 

        self.authenticate(self.manager_user_1)
        response = self.client.get(url)                     #manager get Discount from another branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.authenticate(self.manager_user_2)
        response = self.client.get(url)                     #manager get Discount
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], "You do not have the permission to access this data")





    def test_user_with_no_permission_get_discount(self):
        self.authenticate(self.reception_user_1)
        url = reverse('Get_Discount', kwargs={'pk': 2}) 

        response = self.client.get(url)                     #waiter get Discount
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


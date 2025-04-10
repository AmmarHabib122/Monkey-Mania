from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpDiscountTests import SetUpDataClass









class TestDiscountCreation(SetUpDataClass):
    def test_user_with_no_branch_create_discount(self):
        url = reverse('Create_Discount')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_discount_1, format = 'json') #admin add Discount
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)






    def test_user_with_a_branch_or_no_permission_create_discount(self):
        url = reverse('Create_Discount')
        self.authenticate(self.manager_user_1)
        
        response = self.client.post(url, self.test_discount_2, format = 'json') #waiter add Discount
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














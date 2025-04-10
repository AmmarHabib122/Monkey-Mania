from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpProductBillTests import SetUpDataClass









class TestProductBillCreation(SetUpDataClass):
    def test_user_with_no_branch_create_product_bill(self):
        url = reverse('Create_ProductBill')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_product_bill_1, format = 'json') #admin add ProductBill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_product_bill(self):
        url = reverse('Create_ProductBill')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_product_bill_1, format = 'json') #manager add ProductBill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.authenticate(user = self.reception_user_1)
        response = self.client.post(url, self.test_product_bill_2, format = 'json') #reception add ProductBill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.authenticate(user = self.waiter_user_1)
        response = self.client.post(url, self.test_product_bill_3, format = 'json') #reception add ProductBill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)















    

    














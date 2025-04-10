from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpProductBillTests import SetUpDataClass





class TestProductBillUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_product_bill(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_ProductBill')
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        url = reverse('Update_ProductBill', kwargs = {'pk' : 1})
        
        response = self.client.patch(url, self.test_product_bill_2, format = 'json') #admin update Branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_user_with_a_branch_update_product_bill(self):
        self.authenticate(self.waiter_user_1)
        url = reverse('Create_ProductBill')
        response = self.client.post(url, self.test_product_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('Update_ProductBill', kwargs = {'pk' : 1})
        
        response = self.client.patch(url, self.test_product_bill_1, format = 'json') #waiter update ProductBill
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        



        

    
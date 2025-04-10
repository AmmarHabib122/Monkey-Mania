from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpProductBillTests import SetUpDataClass





class TestProductBillRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_school(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_ProductBill')
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('Get_ProductBill', kwargs={'pk': 1})

        response = self.client.get(url)                     #admin get ProductBill
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_a_branch_get_school(self):
        self.authenticate(user = self.reception_user_1)
        url = reverse('Create_ProductBill')
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('Get_ProductBill', kwargs={'pk': 1}) 

        response = self.client.get(url)                     #reception get ProductBill
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    


    


from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBillTests import SetUpDataClass









class TestBillCreation(SetUpDataClass):
    def test_user_with_no_branch_create_bill(self):
        url = reverse('Create_Bill')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_bill_1, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_bill(self):
        url = reverse('Create_Bill')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_bill_1, format = 'json') #manager add Bill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.authenticate(user = self.reception_user_1)
        response = self.client.post(url, self.test_bill_2, format = 'json') #reception add Bill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_or_no_permission_create_bill(self):
        url = reverse('Create_Bill')
        self.authenticate(self.waiter_user_1)
        
        response = self.client.post(url, self.test_bill_2, format = 'json') #waiter add Bill
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














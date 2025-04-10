from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBillTests import SetUpDataClass





class TestBillRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_bill(self):
        self.authenticate(self.admin_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('Get_Bill', kwargs={'pk': 1})

        response = self.client.get(url)                     #admin get Bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_a_branch_get_bill(self):
        self.authenticate(self.admin_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('Get_Bill', kwargs={'pk': 1})

        response = self.client.get(url)                     #reception get active Bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    # def test_user_with_no_permission_get_bill(self):
    #     self.authenticate(self.waiter_user_1)
    #     url = reverse('Get_Bill', kwargs={'pk': 2}) 

    #     response = self.client.get(url)                     #waiter get Bill
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


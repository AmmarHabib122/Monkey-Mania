from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffTests import SetUpDataClass









class TestStaffCreation(SetUpDataClass):
    def test_user_with_no_branch_create_staff(self):
        url = reverse('Create_Staff')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_staff_1, format = 'multipart') #admin add staff
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.test_staff_2, format = 'multipart') #admin add staff with another branch
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_with_a_branch_create_staff(self):
        url = reverse('Create_Staff')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_staff_1, format = 'multipart') #manager add staff
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.test_staff_2, format = 'multipart') #manager add staff with another branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_user_with_a_branch_or_no_permission_create_staff(self):
        url = reverse('Create_Staff')

        self.authenticate(self.reception_user_1)
        response = self.client.post(url, self.test_staff_2, format = 'multipart') #reception add staff
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.waiter_user_1)
        response = self.client.post(url, self.test_staff_2, format = 'multipart') #waiter add staff
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffTests import SetUpDataClass





class TestStaffRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_staff(self):
        url = reverse('Get_Staff', kwargs={'pk': 2})
        self.authenticate(self.admin_user_1)

        response = self.client.get(url)                     #admin get Staff
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_a_branch_get_staff(self):
        self.authenticate(self.manager_user_1)

        url = reverse('Get_Staff', kwargs={'pk': 1}) 
        response = self.client.get(url)                     #manager get Staff
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_Staff', kwargs={'pk': 2}) 
        response = self.client.get(url)                     #manager get Staff from another branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_user_with_no_permission_get_staff(self):
        self.authenticate(self.reception_user_1)
        url = reverse('Get_Staff', kwargs={'pk': 2}) 

        response = self.client.get(url)                     #reception get Staff
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


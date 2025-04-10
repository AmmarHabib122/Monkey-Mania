from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffTests import SetUpDataClass





class TestStaffUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_staff(self):
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(reverse('Create_Staff'), self.test_staff_1, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_Staff', kwargs = {'pk' : 3})
        self.test_staff_2.pop('branch')
        response = self.client.patch(url, self.test_staff_2, format = 'multipart') #admin update Branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_user_with_a_branch_update_staff(self):
        self.authenticate(self.admin_user_1)
        response = self.client.post(reverse('Create_Staff'), self.test_staff_1, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.authenticate(self.manager_user_1)
        url = reverse('Update_Staff', kwargs = {'pk' : 3})
        self.test_staff_3.pop('branch')
        
        response = self.client.patch(url, self.test_staff_2, format = 'multipart') #manager change staff branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, self.test_staff_3, format = 'multipart') #manager update staff
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        


    def test_user_with_no_permission_update_staff(self):
        self.authenticate(self.admin_user_1)
        response = self.client.post(reverse('Create_Staff'), self.test_staff_1, format = 'multipart')
        self.authenticate(user = self.reception_user_1)
        url = reverse('Update_Staff', kwargs = {'pk' : 3})
        self.test_staff_1.pop('branch')
    
        response = self.client.patch(url, self.test_staff_1, format = 'multipart') #reception update Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    
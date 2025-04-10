from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpSchoolTests import SetUpDataClass









class TestSchoolCreation(SetUpDataClass):
    def test_user_with_no_branch_create_school(self):
        url = reverse('Create_School')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_school_1, format = 'json') #admin add School
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_school(self):
        url = reverse('Create_School')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_school_1, format = 'json') #manager add School
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.authenticate(user = self.reception_user_1)
        response = self.client.post(url, self.test_school_2, format = 'json') #reception add School
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_or_no_permission_create_school(self):
        url = reverse('Create_School')
        self.authenticate(self.waiter_user_1)
        
        response = self.client.post(url, self.test_school_2, format = 'json') #waiter add School
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














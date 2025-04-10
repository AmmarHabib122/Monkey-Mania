from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpUserTests import SetUpDataClass





class TestUserRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_user(self):
        self.authenticate(self.admin_user_2)

        url = reverse('Get_User', kwargs={'pk': 7})  #admin get himself
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': 5})  #admin get waiter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': 4})  #admin get reception
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': 3})  #admin get manager
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': 2})  #admin get admin
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': 1})  #admin get owner
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    



    def test_user_with_a_branch_get_user(self):
        self.authenticate(self.manager_user_1)

        url = reverse('Get_User', kwargs={'pk': 3})  #manager get himself
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': 10})  #manager get waiter from another branch
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': 4})  #manager get reception
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': 8})  #manager get manager 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': 2})  #manager get admin
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': 1})  #manager get owner
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_user_with_no_permission_get_user(self):
        self.authenticate(self.reception_user_1)

        url = reverse('Get_User', kwargs={'pk': 4})  #reception get himself
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': 5})  #reception get waiter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


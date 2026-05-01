from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpUserTests import SetUpDataClass







class TestUserRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_user(self):
        self.authenticate(self.admin_user_2)

        url = reverse('Get_User', kwargs={'pk': self.admin_user_2.id})  #admin get himself
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': self.waiter_user_1.id})  #admin get waiter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': self.reception_user_1.id})  #admin get reception
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': self.manager_user_1.id})  #admin get manager
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': self.admin_user_1.id})  #admin get admin
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': self.owner_user_1.id})  #admin get owner
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_user_with_a_branch_get_user(self):
        self.authenticate(self.manager_user_1)

        url = reverse('Get_User', kwargs={'pk': self.manager_user_1.id})  #manager get himself
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': self.waiter_user_2.id})  #manager get waiter from another branch
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': self.reception_user_1.id})  #manager get reception
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_User', kwargs={'pk': self.manager_user_2.id})  #manager get manager
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': self.admin_user_1.id})  #manager get admin
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': self.owner_user_1.id})  #manager get owner
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_user_with_no_permission_get_user(self):
        self.authenticate(self.reception_user_1)

        url = reverse('Get_User', kwargs={'pk': self.reception_user_1.id})  #reception get himself
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_User', kwargs={'pk': self.waiter_user_1.id})  #reception get waiter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





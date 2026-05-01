from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpUserTests import SetUpDataClass







class TestUserUpdate(SetUpDataClass):
    def test_user_with_no_branch_udpate_user(self):
        self.authenticate(self.admin_user_1)

        data = {
            'username': 'newwaiter',
            'phone_number': '17534682951',
            'password': 'sadflkjAh',
            'confirm_password': 'sadflkjAh',
            'role': 'waiter',
            'branch': self.branch_2.id,
        }
        url = reverse('Update_User', kwargs = {'pk' : self.manager_user_1.id})             #update a manager to a waiter
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data['role'] = 'manager'
        url = reverse('Update_User', kwargs = {'pk' : self.manager_user_1.id})             #update a waiter to a manager
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data['role'] = 'owner'
        url = reverse('Update_User', kwargs = {'pk' : self.manager_user_1.id})             #update a manager to an owner
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'admin'
        url = reverse('Update_User', kwargs = {'pk' : self.manager_user_1.id})             #update a manager to an admin
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        data['username'] = 'anodsfther'
        data['phone_number'] = '01030261325'
        url = reverse('Update_User', kwargs = {'pk' : self.owner_user_1.id})             #update a higher-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : self.admin_user_2.id})             #update an equal-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_user_with_a_branch_udpate_user(self):
        self.authenticate(self.manager_user_1)

        data = {
            'username': 'newreception',
            'phone_number': '17504682951',
            'password': 'sadflkjAh',
            'confirm_password': 'sadflkjAh',
            'role': 'reception',
            'branch': self.branch_2.id,
        }
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a waiter to a reception
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data['role'] = 'manager'
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a reception to a manager
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'owner'
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a reception to an owner
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'admin'
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a reception to an admin
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['username']    = 'another'
        data['phone_number'] = '01030261325'
        data['role']         = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : self.admin_user_1.id})             #update a higher-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : self.manager_user_2.id})             #update an equal-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_user_with_no_permission_update_user(self):
        self.authenticate(self.reception_user_1)

        data = {
            'username': 'newreception',
            'phone_number': '17504682951',
            'password': 'sadflkjAh',
            'confirm_password': 'sadflkjAh',
            'role': 'reception',
            'branch': self.branch_2.id,
        }
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a waiter to a reception
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a waiter to a waiter
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'manager'
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a waiter to a manager
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'owner'
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a waiter to an owner
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'admin'
        url = reverse('Update_User', kwargs = {'pk' : self.waiter_user_1.id})             #update a waiter to an admin
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        data['username'] = 'another'
        data['phone_number'] = '01030261325'
        url = reverse('Update_User', kwargs = {'pk' : self.manager_user_1.id})             #update a higher-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : self.reception_user_2.id})             #update an equal-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : self.reception_user_1.id})             #reception update himself but only the pass will be changed
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        update_own = {
            'password' : 'helpasdfdsaf',
            'confirm_password' : "helpasdfdsaf",
            'branch' : self.branch_2.id
        }
        url = reverse('Update_User', kwargs = {'pk' : self.reception_user_1.id})             #reception update his password
        response = self.client.patch(url, update_own, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


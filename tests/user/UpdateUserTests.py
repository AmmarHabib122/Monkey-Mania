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
            'branch': 2,
        }
        url = reverse('Update_User', kwargs = {'pk' : 3})             #update a manager to a waiter
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data['role'] = 'manager'
        url = reverse('Update_User', kwargs = {'pk' : 3})             #update a waiter to a manager
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data['role'] = 'owner'
        url = reverse('Update_User', kwargs = {'pk' : 3})             #update a manager to an owner
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'admin'
        url = reverse('Update_User', kwargs = {'pk' : 3})             #update a manager to an admin
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        data['username'] = 'anodsfther'
        data['phone_number'] = '01030261325'
        url = reverse('Update_User', kwargs = {'pk' : 1})             #update a higher-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : 7})             #update an equal-role-user
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
            'branch': 2,
        }
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a waiter to a reception
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data['role'] = 'manager'
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a reception to a manager
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'owner'
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a reception to an owner
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'admin'
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a reception to an admin
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['username']    = 'another'
        data['phone_number'] = '01030261325'
        data['role']         = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : 2})             #update a higher-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : 8})             #update an equal-role-user
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
            'branch': 2,
        }
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a waiter to a reception
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a waiter to a waiter
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'manager'
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a waiter to a manager
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'owner'
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a waiter to an owner
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'admin'
        url = reverse('Update_User', kwargs = {'pk' : 5})             #update a waiter to an admin
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        data['username'] = 'another'
        data['phone_number'] = '01030261325'
        url = reverse('Update_User', kwargs = {'pk' : 3})             #update a higher-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : 9})             #update an equal-role-user
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['role'] = 'waiter'
        url = reverse('Update_User', kwargs = {'pk' : 4})             #reception update himself but only the pass will be changed
        response = self.client.patch(url, data, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        update_own = {
            'password' : 'helpasdfdsaf',
            'confirm_password' : "helpasdfdsaf",
            'branch' : 2
        }
        url = reverse('Update_User', kwargs = {'pk' : 4})             #reception update his password
        response = self.client.patch(url, update_own, format = 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


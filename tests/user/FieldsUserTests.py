from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpUserTests import SetUpDataClass












class TestUserFields(SetUpDataClass):
    def test_password(self):
        url = reverse('Create_User')
        self.authenticate(self.admin_user_1)

        self.test_waiter_user_2['password'] = '123456789'
        self.test_waiter_user_2['confirm_password'] = '123456789'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['message'].lower())

        self.test_waiter_user_2['password'] = '12345'
        self.test_waiter_user_2['confirm_password'] = '12345'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['message'].lower())

        self.test_waiter_user_2['password'] = '123456Ah'
        self.test_waiter_user_2['confirm_password'] = '123456Ahd'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['message'].lower())




    def test_username(self):
        url = reverse('Create_User')
        self.authenticate(self.admin_user_1)
        response = self.client.post(url, self.test_reception_user_2, format = 'multipart') 

        self.test_waiter_user_2['username'] = self.test_reception_user_2['username']
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data['message'].lower())

        self.test_waiter_user_2['username'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('150 characters', response.data['message'].lower())




    def test_phone_number(self):
        url = reverse('Create_User')
        self.authenticate(self.admin_user_1)
        response = self.client.post(url, self.test_reception_user_2, format = 'multipart') 

        self.test_waiter_user_2['phone_number'] = self.test_reception_user_2['phone_number']
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone number', response.data['message'].lower())

        self.test_waiter_user_2['phone_number'] = '6513'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone number', response.data['message'].lower())

        self.test_waiter_user_2['phone_number'] = '65464641654165'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone number', response.data['message'].lower())

        self.test_waiter_user_2['phone_number'] = '1265423568h'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone number', response.data['message'].lower())



        
    def test_email(self):
        url = reverse('Create_User')
        self.authenticate(self.admin_user_1)
        self.test_reception_user_2['email'] = 'asdf@gmail.com'
        response = self.client.post(url, self.test_reception_user_2, format = 'multipart') 

        self.test_waiter_user_2['email'] = self.test_reception_user_2['email']
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['message'].lower())

        self.test_waiter_user_2['email'] = 'sdafasdlkfhs'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['message'].lower())

        self.test_waiter_user_2['email'] = 'ahmed@gmail'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['message'].lower())




    def test_branch(self):
        url = reverse('Create_User')
        self.authenticate(self.admin_user_1)

        self.test_waiter_user_2['branch'] = 35
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Selected branch does not exist.', response.data['message'])

        self.test_waiter_user_2['branch'] = 'a'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Branch must be identified by an integer ID.', response.data['message'])




    def test_role(self):
        url = reverse('Create_User')
        self.authenticate(self.admin_user_1)

        self.test_waiter_user_2['role'] = 'heflkasdh'
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('role', response.data['message'].lower())
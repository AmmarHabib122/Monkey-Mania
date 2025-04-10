from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from base import models
from .SetUpUserTests import SetUpDataClass





class TestUserListRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_all_users(self):
        self.authenticate(self.owner_user_2)

        resverse_url = reverse('List_User')       #get users from all branches
        query_params = {
            'search': '',  
            'branch_id': [1, 2]  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

        resverse_url = reverse('List_User')       #get users from all branches with user name contains manager
        query_params = {
            'search': 'manager',  
            'branch_id': [1, 2]  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        resverse_url = reverse('List_User')       #get users with invalid branches
        query_params = {
            'search': '',  
            'branch_id': [1, 3, 5]  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




    def test_user_with_a_branch_get_all_users(self):
        self.authenticate(self.manager_user_2)

        resverse_url = reverse('List_User')       #get users from the manager branch although multiple branch ids are provided
        query_params = {
            'search': '',  
            'branch_id': [1, 2]  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        resverse_url = reverse('List_User')       #get users from the manager branch although multiple branch ids are provided with user name contains waiter
        query_params = {
            'search': 'waiter',  
            'branch_id': [1, 2]  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        
        

    def test_user_with_no_permission_get_user(self):
        self.authenticate(self.reception_user_1)

        resverse_url = reverse('List_User')       
        query_params = {
            'search': '',  
            'branch_id': [1, 2]  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


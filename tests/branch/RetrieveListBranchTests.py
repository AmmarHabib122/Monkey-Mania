from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from base import models
from .SetUpBranchTests import SetUpDataClass





class TestBranchListRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_all_branches(self):
        self.authenticate(self.admin_user_1)

        resverse_url = reverse('List_Branch')       #admin get all branch with name = branch1
        query_params = {
            'search': 'Branch1',  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        resverse_url = reverse('List_Branch')       #admin get all branches
        query_params = {
            'search': '',  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


        

    def test_user_with_no_permission_get_all_branch(self):
        self.authenticate(self.reception_user_1)

        resverse_url = reverse('List_Branch')       #reception get all branches
        query_params = {
            'search': '',  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


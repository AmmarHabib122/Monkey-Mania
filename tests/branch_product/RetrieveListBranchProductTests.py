from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from base import models
from .SetUpBranchProductTests import SetUpDataClass





class TestBranchProductListRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_all_branch_products(self):
        self.authenticate(self.admin_user_1)

        resverse_url = reverse('List_BranchProduct')       #admin get all BranchProduct with name = branch_product1
        query_params = {
            'search': 'pistachio',  
            'branch_id' : 1
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        resverse_url = reverse('List_BranchProduct')       #admin get all BranchProductes from  branch 1
        query_params = {
            'search': '',  
            'branch_id' : 2
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)




    def test_user_with_a_branch_get_all_branch_products(self):
        self.authenticate(self.manager_user_1)

        resverse_url = reverse('List_BranchProduct')       #manager get all BranchProductes from his branch
        query_params = {
            'search': '',  
            'branch_id' : 1
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        resverse_url = reverse('List_BranchProduct')       #manager get all BranchProductes from another branch but get his branch
        query_params = {
            'search': '',  
            'branch_id' : 2
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


        

    def test_user_with_no_permission_get_all_BranchProduct(self):
        self.authenticate(self.waiter_user_1)

        resverse_url = reverse('List_BranchProduct')       #manager get all BranchProductes
        query_params = {
            'search': '',  
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchProductTests import SetUpDataClass





class TestBranchProductRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_branch_product(self):
        url = reverse('Get_BranchProduct', kwargs={'pk': 2})
        self.authenticate(self.admin_user_1)

        response = self.client.get(url)                     #admin get BranchProduct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_a_branch_get_branch_product(self):
        self.authenticate(self.manager_user_1)

        url = reverse('Get_BranchProduct', kwargs={'pk': 2}) 
        response = self.client.get(url)                     #manager get BranchProduct from his branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_BranchProduct', kwargs={'pk': 1}) 
        response = self.client.get(url)                     #manager get BranchProduct from another branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





    def test_user_with_no_permission_get_branch_product(self):
        self.authenticate(self.waiter_user_1)
        url = reverse('Get_BranchProduct', kwargs={'pk': 2}) 

        response = self.client.get(url)                     #waiter get BranchProduct
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


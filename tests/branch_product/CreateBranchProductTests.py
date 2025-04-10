from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchProductTests import SetUpDataClass









class TestBranchProductCreation(SetUpDataClass):
    def test_user_with_no_branch_add_product_to_branch(self):
        url = reverse('Create_BranchProduct')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_branch_product_1, format = 'json') #admin add BranchProduct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_branch_product_2['branch'] = self.test_branch_product_1['branch']
        self.test_branch_product_2['product'] = self.test_branch_product_1['product']
        response = self.client.post(url, self.test_branch_product_2, format = 'json') #admin add duplicte BranchProduct
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('unique set', response.data['message'].lower())




    def test_user_with_a_branch_add_product_to_branch(self):
        url = reverse('Create_BranchProduct')
        self.authenticate(user = self.manager_user_1)

        response = self.client.post(url, self.test_branch_product_1, format = 'json') #manager add BranchProduct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.test_branch_product_3, format = 'json') #manager add material form another branch to a BranchProduct 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("You Can not access a material from another branch", response.data['message'])




    def test_user_with_a_branch_or_no_permission_add_product_to_branch(self):
        url = reverse('Create_BranchProduct')
        self.authenticate(self.reception_user_1)
        
        response = self.client.post(url, self.test_branch_product_1, format = 'json') #reception add BranchProduct
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchTests import SetUpDataClass





class TestBranchRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_branch(self):
        self.authenticate(self.admin_user_1)

        url = reverse('Get_Branch', kwargs={'pk': 2})  #admin get Branch
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_manager_get_branch(self):
        self.authenticate(self.manager_user_1)

        url = reverse('Get_Branch', kwargs={'pk': 1})  #manager get his managed branch
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Get_Branch', kwargs={'pk': 3})  #manager get aonther barnch
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        




    def test_user_with_no_permission_get_branch(self):
        self.authenticate(self.reception_user_1)

        url = reverse('Get_Branch', kwargs={'pk': 1})  #reception get the barnch he is in
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Get_Branch', kwargs={'pk': 2})  #reception get another branch
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


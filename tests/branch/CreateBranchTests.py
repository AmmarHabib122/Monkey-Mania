from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchTests import SetUpDataClass









class TestBranchCreation(SetUpDataClass):
    def test_user_with_no_branch_create_branch(self):
        url = reverse('Create_Branch')
        self.authenticate(user = self.admin_user_1)
        
        self.test_branch_1.pop('manager')
        response = self.client.post(url, self.test_branch_1, format = 'json') #admin add Branch
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_or_no_permission_create_branch(self):
        url = reverse('Create_Branch')
        self.authenticate(self.manager_user_1)
        
        self.test_branch_2.pop('manager')
        response = self.client.post(url, self.test_branch_2, format = 'json') #manager add Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














    # def test_user_username(self):
    #     url = reverse('Create_User')
    #     self.authenticate(self.admin_user_1)
    #     response = self.client.post(url, self.test_waiter_user_2, format = 'json')

    #     self.test_reception_user_2['username'] = self.test_waiter_user_2['username']
    #     response = self.client.post(url, self.test_reception_user_2, format = 'json') 
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     with self.assertRaises(IntegrityError):
    #         response

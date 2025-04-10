from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpChildTests import SetUpDataClass





class TestChildUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_child(self):
        self.authenticate(user = self.admin_user_1)
        
        url = reverse('Update_Child', kwargs = {'pk' : 1})
        response = self.client.patch(url, self.test_child_1, format = 'json') #admin update Branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)






    def test_user_with_a_branch_update_child(self):
        url = reverse('Update_Child', kwargs = {'pk' : 2})
        self.authenticate(self.reception_user_1)
        
        response = self.client.patch(url, self.test_child_2, format = 'json') #reception update Child
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['child_phone_numbers_set']), 2)

        response = self.client.patch(url, self.test_child_3, format = 'json') #reception update Child
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['child_phone_numbers_set']), 2)

        
        self.test_child_1['child_phone_numbers_set'] = []
        response = self.client.patch(url, self.test_child_1, format = 'json') #reception update Child
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.manager_user_1)
        self.test_child_1['child_phone_numbers_set'] = []
        response = self.client.patch(url, self.test_child_1, format = 'json') #manager update Child
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        


    def test_user_with_no_permission_update_child(self):
        self.authenticate(user = self.waiter_user_1)
        
        url = reverse('Update_Child', kwargs = {'pk' : 1})
        response = self.client.patch(url, self.test_child_1, format = 'json') #waiter update Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    
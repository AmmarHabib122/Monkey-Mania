from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpChildTests import SetUpDataClass





class TestChildRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_child(self):
        self.authenticate(self.admin_user_1)

        url = reverse('Get_Child', kwargs={'pk': 1})  #admin get Child
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    

    def test_user_with_a_branch_get_child(self):

        self.authenticate(self.manager_user_1)
        url = reverse('Get_Child', kwargs={'pk': 1})  #manager get  Child
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.authenticate(self.reception_user_1)
        url = reverse('Get_Child', kwargs={'pk': 1})  #recepetion get Child
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        




    def test_user_with_no_permission_get_child(self):
        self.authenticate(self.waiter_user_1)
        
        url = reverse('Get_Child', kwargs={'pk': 1})  #waiter get child
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


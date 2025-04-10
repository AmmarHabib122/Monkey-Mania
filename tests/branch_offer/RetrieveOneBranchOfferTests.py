from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchOfferTests import SetUpDataClass





class TestBranchOfferRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_branch_offer(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Get_BranchOffer', kwargs={'pk': 1})

        response = self.client.get(url)                     #admin get BranchOffer
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_a_branch_get_branch_offer(self):
        self.authenticate(user = self.manager_user_1)
        url = reverse('Get_BranchOffer', kwargs={'pk': 1}) 

        response = self.client.get(url)                     #reception get BranchOffer
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_user_with_no_permission_get_branch_offer(self):
        self.authenticate(user = self.reception_user_1)
        url = reverse('Get_BranchOffer', kwargs={'pk': 1}) 

        response = self.client.get(url)                     #reception get BranchOffer
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





    


    


from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchOfferTests import SetUpDataClass





class TestBranchOfferUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_branch_offer(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Update_BranchOffer', kwargs = {'pk' : 1})
        
        response = self.client.patch(url, self.test_branch_offer_2, format = 'json') #admin update BranchOffer
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_user_with_a_branch_update_branch_offer(self):
        self.authenticate(self.manager_user_1)
        url = reverse('Update_BranchOffer', kwargs = {'pk' : 1})
        
        response = self.client.patch(url, self.test_branch_offer_1, format = 'json') #waiter update BranchOffer
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_user_with_no_permission_update_branch_offer(self):
        self.authenticate(self.reception_user_1)
        url = reverse('Update_BranchOffer', kwargs = {'pk' : 1})
        
        response = self.client.patch(url, self.test_branch_offer_1, format = 'json') #waiter update BranchOffer
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



        



        

    
from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchOfferTests import SetUpDataClass









class TestBranchOfferCreation(SetUpDataClass):
    def test_user_with_no_branch_create_branch_offer(self):
        url = reverse('Create_BranchOffer')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_branch_offer_1, format = 'json') #admin add BranchOffer
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_branch_offer(self):
        url = reverse('Create_BranchOffer')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_branch_offer_1, format = 'json') #manager add BranchOffer
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        



    def test_user_with_no_permission_create_branch_offer(self):
        url = reverse('Create_BranchOffer')
        
        self.authenticate(user = self.reception_user_1)
        response = self.client.post(url, self.test_branch_offer_1, format = 'json') #manager add BranchOffer
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)















    

    














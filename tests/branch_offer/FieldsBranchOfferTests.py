from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchOfferTests import SetUpDataClass












class TestBranchOfferFields(SetUpDataClass):
    def test_before_sale_price(self):
        url = reverse('Create_BranchOffer')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_branch_offer_1, format = 'json') #admin add BranchOffer
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['before_sale_price']), 350)







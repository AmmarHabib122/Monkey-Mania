from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBillTests import SetUpDataClass





class TestBillClosing(SetUpDataClass):
    def test_user_with_no_branch_close_bill(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        url = reverse('Close_Bill', kwargs = {'pk' : 1})
        data = {
            'visa' : 255
        }
        response = self.client.patch(url, data, format = 'json') #admin close bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['money_unbalance'], 255)




    def test_user_with_a_branch_close_bill(self):
        self.authenticate(self.reception_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        url = reverse('Close_Bill', kwargs = {'pk' : 1})
        data = {
            'visa' : 255
        }
        response = self.client.patch(url, data, format = 'json') #recpeiton close bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['money_unbalance'], 255)



        


    def test_user_with_no_permission_close_bill(self):
        self.authenticate(self.waiter_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')

        url = reverse('Close_Bill', kwargs = {'pk' : 1})
        data = {
            'visa' : 255
        }
        response = self.client.patch(url, data, format = 'json') #recpeiton close bill 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    










class TestBillApplyDiscount(SetUpDataClass):
    def test_user_with_no_branch_apply_discount_bill(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        url = reverse('Apply_Discount_Bill', kwargs = {'pk' : 1})
        data = {
            'discount' : 'promo1',
        }
        response = self.client.patch(url, data, format = 'json') #admin apply_discount bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['discount_value']), 0.70)
        self.assertEqual(response.data['discount_type'], "percentage")




    def test_user_with_a_branch_apply_discount_bill(self):
        self.authenticate(self.manager_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        url = reverse('Apply_Discount_Bill', kwargs = {'pk' : 1})
        data = {
            'discount' : 'promo2',
        }
        response = self.client.patch(url, data, format = 'json') #admin apply_discount bill
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Couldn't find a discount available to this branch with the given credentials.")

        url = reverse('Apply_Discount_Bill', kwargs = {'pk' : 1})
        data = {
            'discount' : 'sadfasdfasdf',
        }
        response = self.client.patch(url, data, format = 'json') #admin apply_discount bill
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Couldn't find a discount available to this branch with the given credentials.")

        url = reverse('Apply_Discount_Bill', kwargs = {'pk' : 1})
        data = {
            'discount' : 'promo1',
        }
        response = self.client.patch(url, data, format = 'json') #admin apply_discount bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['discount_value']), 0.70)
        self.assertEqual(response.data['discount_type'], "percentage")




        


    def test_user_with_no_permission_apply_discount_bill(self):
        self.authenticate(self.reception_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')

        url = reverse('Apply_Discount_Bill', kwargs = {'pk' : 1})
        data = {
            'discount' : 'promo1',
        }
        response = self.client.patch(url, data, format = 'json') #recpeiton apply_discount bill 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
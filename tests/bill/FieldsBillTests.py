from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBillTests import SetUpDataClass


    









class TestBillFields(SetUpDataClass):
    def test_cash(self):
        ...




    def test_visa(self):
        ...

    


    def test_instapay(self):
        ...
        


    def test_time_price(self):
        ...



    def test_discount(self):
        url = reverse('Create_Bill')
        self.authenticate(self.admin_user_1)

        self.test_bill_1['discount'] = 'afsdfkhasdlfk'
        response = self.client.post(url, self.test_bill_1, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Couldn't find a discount available to this branch with the given credentials.")
        
        self.test_bill_1['discount'] = 'promo2'
        response = self.client.post(url, self.test_bill_1, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Couldn't find a discount available to this branch with the given credentials.")

        self.test_bill_1['discount'] = 'promo1'
        response = self.client.post(url, self.test_bill_1, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['discount_value']), 0.70)
        self.assertEqual(response.data['discount_type'], "percentage")
        self.assertEqual(float(response.data['hour_price']), 35)
        self.assertEqual(float(response.data['half_hour_price']), 20)

        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Close_Bill', kwargs = {'pk' : 2})
        data = {
            'visa' : 255
        }
        response = self.client.patch(url, data, format = 'json') #admin close bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('Apply_Discount_Bill', kwargs = {'pk' : 1})
        data = {
            'discount' : 'promo1',
        }
        response = self.client.patch(url, data, format = 'json') #admin apply_discount bill
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['discount_value']), 0.70)
        self.assertEqual(response.data['discount_type'], "percentage")





    def test_full_and_half_hour_price(self):
        url = reverse('Create_Bill')
        self.authenticate(self.admin_user_1)

        self.test_bill_1['children'] = [1, 2, 3, 4, 5]
        response = self.client.post(url, self.test_bill_1, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "There is no hour prices found for 5 children in this branch.")
        



    def test_money_unbalance(self):
        url = reverse('Create_Bill')
        self.authenticate(self.admin_user_1)
        response = self.client.post(url, self.test_bill_1, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, self.test_bill_2, format = 'json') #admin add Bill
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Close_Bill', kwargs = {'pk' : 1})
        data = {
            'cash'        : 150,
            'visa'        : 25,
            'instapay'    : 25,
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['money_unbalance']), 200)

        






    def test_children(self):
        url = reverse('Create_Bill')
        self.authenticate(self.admin_user_1)

        children = self.test_bill_1.pop('children', [])
        self.test_bill_1['children'] = []
        response = self.client.post(url, self.test_bill_1, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Children list can not be empty")

        self.test_bill_1['children'] = children
        self.test_bill_1['children'].append(1)
        response = self.client.post(url, self.test_bill_1, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "You tried to add the same child more than once")

        self.test_bill_1['children'].pop(0)
        response = self.client.post(url, self.test_bill_1, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['hour_price']), 120)
        self.assertEqual(float(response.data['half_hour_price']), 70)

        response = self.client.post(url, self.test_bill_2, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['hour_price']), 170)
        self.assertEqual(float(response.data['half_hour_price']), 100)

        response = self.client.post(url, self.test_bill_duplicate, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Child child1 is currently registered in another bill")

        self.test_bill_duplicate['branch'] = 1
        response = self.client.post(url, self.test_bill_duplicate, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Child child1 is currently registered in another bill")

        


    
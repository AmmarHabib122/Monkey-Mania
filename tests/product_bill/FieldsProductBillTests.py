from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpProductBillTests import SetUpDataClass












class TestProductBillFields(SetUpDataClass):
    def test_table_number(self):
        ...

    def test_take_away(self):
        ...

    def test_bill(self):
        ...

    def test_total_price(self):
        self.authenticate(user = self.admin_user_1)

        url = reverse('Create_ProductBill')
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total_price']), 950)

        url = reverse('Update_ProductBill', kwargs = {'pk' : 1})

        data = {
            'returned_products' : [
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 2,
                },
                {
                    'product_type'  : 'product',
                    'product_id'  : 2,
                    'quantity' : 3,
                },
            ]
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_price']), 300)

        response = self.client.patch(url, self.test_product_bill_2, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_price']), 1450)





    def test_products(self):
        self.authenticate(user = self.admin_user_1)

        url = reverse('Create_ProductBill')
        self.test_product_bill_1['products'].append(
            {
                'product_type'  : 'product',
                'product_id'  : 1,
                'quantity' : 3,
                'notes' : 'help'
            },
        )
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Duplicate added items detected")

        self.test_product_bill_1['products'].pop(-1)
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_ProductBill', kwargs = {'pk' : 1})

        data = {
            'products' : [
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 2,
                    'notes' : 'help'
                },
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 3,
                    'notes' : 'help'
                },
                
            ]
        }
        response = self.client.patch(url, {"products" : []}, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "At least one added item must be provided")

        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Duplicate added items detected")







    def test_returned_products(self):
        self.authenticate(user = self.admin_user_1)

        url = reverse('Create_ProductBill')
        self.test_product_bill_1['returned_products'] = [
            {
                'product_type'  : 'product',
                'product_id'  : 1,
                'quantity' : 3,
            },
        ]
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "You cannot return items when creating a bill.")

        self.test_product_bill_1.pop("returned_products")
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_ProductBill', kwargs = {'pk' : 1})

        data = {
            'returned_products' : [
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 2,
                },
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 3,
                },
                
            ]
        }
        response = self.client.patch(url, {"returned_products" : []}, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "At least one returned item must be provided")

        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Duplicate returned items detected")

        data = {
            'returned_products' : [
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 2,
                },
                {
                    'product_type'  : 'product',
                    'product_id'  : 2,
                    'quantity' : 6,
                },
                
            ]
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Not enough tajin pistachio units to return")

        data = {
            'returned_products' : [
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 2,
                },
                {
                    'product_type'  : 'product',
                    'product_id'  : 2,
                    'quantity' : 4,
                },
                
            ]
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'returned_products' : [
                {
                    'product_type'  : 'product',
                    'product_id'  : 1,
                    'quantity' : 1,
                },   
            ]
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Not enough waffle nutella units to return")






    







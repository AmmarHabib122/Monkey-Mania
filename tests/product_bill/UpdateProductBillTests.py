from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpProductBillTests import SetUpDataClass





class TestProductBillUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_product_bill(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_ProductBill')
        response = self.client.post(url, self.test_product_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_ProductBill', kwargs = {'pk' : 1})

        response = self.client.patch(url, {'returned_products': [
            {'product_type': 'product', 'product_id': 1, 'quantity': 1}
        ]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(float(response.data['total_price']), 950)
        product_bill = models.ProductBill.objects.get(pk=1)
        self.assertEqual(product_bill.products.get(product_id=1).quantity, 1)
        self.assertEqual(product_bill.returned_products.count(), 1)




    def test_user_with_a_branch_update_product_bill(self):
        self.authenticate(self.waiter_user_1)
        url = reverse('Create_ProductBill')
        response = self.client.post(url, self.test_product_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('Update_ProductBill', kwargs = {'pk' : 1})

        response = self.client.patch(url, {'returned_products': [
            {'product_type': 'product', 'product_id': 1, 'quantity': 1}
        ]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(float(response.data['total_price']), 1150)
        self.assertEqual(models.ProductBill.objects.get(pk=1).products.get(product_id=1).quantity, 3)

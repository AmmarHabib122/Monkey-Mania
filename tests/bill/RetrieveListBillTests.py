from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from base import models
from .SetUpBillTests import SetUpDataClass




class TestBillListRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_all_billes(self):
        self.authenticate(self.admin_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bill_id_1 = response.data['id']
        response = self.client.post(url, self.test_bill_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('Close_Bill', kwargs = {'pk' : bill_id_1})
        data = {
            'cash'        : 150,
            'visa'        : 0,
            'instapay'    : 0,
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        resverse_url = reverse('List_Bill')       #admin get all Bill with child name = child3
        query_params = {
            'search': 'child3',
            'branch_id' : self.branch_1.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        resverse_url = reverse('List_Bill')       #admin get all Billes
        query_params = {
            'search': '',
            'branch_id' : self.branch_1.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)




    def test_user_with_no_permission_get_all_Bill(self):
        self.authenticate(self.reception_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bill_id = response.data['id']
        url = reverse('Close_Bill', kwargs = {'pk' : bill_id})
        data = {
            'cash'        : 150,
            'visa'        : 0,
            'instapay'    : 0,
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.authenticate(self.waiter_user_1)
        resverse_url = reverse('List_Bill')       #reception get all Billes
        query_params = {
            'search': '',
            'branch_id' : self.branch_1.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




class TestActiveBillListRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_all_billes(self):
        self.authenticate(self.admin_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        resverse_url = reverse('List_ActiveBill')       #admin get all Bill with child name = child3
        query_params = {
            'search': 'child3',
            'branch_id' : self.branch_1.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        resverse_url = reverse('List_ActiveBill')       #admin get all Billes
        query_params = {
            'search': '',
            'branch_id' : self.branch_1.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        resverse_url = reverse('List_ActiveBill')       #admin get all Billes in another branch
        query_params = {
            'search': '',
            'branch_id' : self.branch_2.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)




    def test_user_with_a_branch_get_all_billes(self):
        self.authenticate(self.reception_user_1)
        url = reverse('Create_Bill')
        response = self.client.post(url, self.test_bill_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        resverse_url = reverse('List_ActiveBill')       #reception get all Billes
        query_params = {
            'search': '',
            'branch_id' : self.branch_1.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.authenticate(self.waiter_user_1)
        resverse_url = reverse('List_ActiveBill')       #waiter get all Billes
        query_params = {
            'search': '',
            'branch_id' : self.branch_1.id
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from base import models
from .SetUpDiscountTests import SetUpDataClass





class TestDiscountListRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_all_discountes(self):
        self.authenticate(self.admin_user_1)

        resverse_url = reverse('List_Discount')       #admin get all Discount with name = discounte1
        query_params = {
            'search': 'promo1',  
            'branch_id' : '1'
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        resverse_url = reverse('List_Discount')       #admin get all Discountes
        query_params = {
            'search' : '',  
            'branch_id' : '1'
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)




    def test_user_with_a_branch_get_all_discountes(self):
        self.authenticate(self.manager_user_2)

        resverse_url = reverse('List_Discount')       #reception get all Discountes
        query_params = {
            'search': '',  
            'branch_id' : '1'
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


        

    def test_user_with_no_permission_get_all_Discount(self):
        self.authenticate(self.waiter_user_1)

        resverse_url = reverse('List_Discount')       #reception get all Discountes
        query_params = {
            'search': '',  
            'branch_id' : '1'
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


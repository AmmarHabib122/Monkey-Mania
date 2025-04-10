from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchProductTests import SetUpDataClass












class TestBranchProductFields(SetUpDataClass):
    def test_product(self):
        ...




    def test_branch(self):
        ...
    


    def test_warning_units(self):
        ...
        


    def test_price(self):
        ...



    def test_material_consumptions_set(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_BranchProduct')
        data = {}
        
        data = self.test_branch_product_1.copy()
        data.pop('material_consumptions_set')
        response = self.client.post(url, data, format = 'json')      #admin add BranchProduct with null materials
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The field 'material_consumptions_set' is required.", response.data['message'])

        data['material_consumptions_set'] = []
        response = self.client.post(url, data, format = 'json')      #admin add BranchProduct with empty materials
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Materials must be provided.", response.data['message'])
        
        data.clear()
        url = reverse('Update_BranchProduct', kwargs = {'pk' : 1})  

        data['material_consumptions_set'] = self.test_branch_product_1['material_consumptions_set']
        response = self.client.patch(url, data, format = 'json')     #admin add material
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['material_consumptions_set']), 2)

        data['material_consumptions_set'].pop(0)
        response = self.client.patch(url, data, format = 'json')     #admin remove first mterial
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['material_consumptions_set']), 1)

        data['material_consumptions_set'].pop(0)
        response = self.client.patch(url, data, format = 'json')     #admin remove first mterial
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Materials must be provided.", response.data['message'])


    


    def test_warning_message(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_BranchProduct')

        response = self.client.post(url, self.test_branch_product_1, format = 'json')   
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['available_units'], 100)
        # self.assertEqual(None, response.data['warning_message'])
        self.assertIn("Check material", response.data['warning_message'])



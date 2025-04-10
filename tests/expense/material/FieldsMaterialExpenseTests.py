from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpMaterialExpenseTests import SetUpDataClass












class TestMaterialExpenseFields(SetUpDataClass):
    def test_material(self):
        ...




    def test_unit_price(self):
       ...

    


    def test_total_price(self):
        ...



    def test_quantity(self):
        self.authenticate(user = self.admin_user_1)

        url = reverse('Get_BranchMaterial', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['available_units']), 15)

        url = reverse('Create_MaterialExpense')
        response = self.client.post(url, self.test_material_expense_1, format = 'json') #admin add MaterialExpense
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Get_BranchMaterial', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['available_units']), 25)

        



    def test_branch(self):
        ...
        



    
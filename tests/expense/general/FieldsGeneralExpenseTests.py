from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpGeneralExpenseTests import SetUpDataClass












class TestGeneralExpenseFields(SetUpDataClass):
    def test_name(self):
        ...




    def test_unit_price(self):
        url = reverse('Create_GeneralExpense')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_general_expense_1, format = 'json') #admin add GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['unit_price']), 1000)

        response = self.client.post(url, self.test_general_expense_3, format = 'json') #admin add GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['unit_price']), 200)

    


    def test_total_price(self):
        ...


    
    def test_quantity(self):
        ...
        


    def test_branch(self):
        ...



    
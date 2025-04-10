from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpMaterialExpenseTests import SetUpDataClass









class TestMaterialExpenseCreation(SetUpDataClass):
    def test_user_with_no_branch_create_material_expense(self):
        url = reverse('Create_MaterialExpense')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_material_expense_1, format = 'json') #admin add MaterialExpense
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_material_expense(self):
        url = reverse('Create_MaterialExpense')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_material_expense_1, format = 'json') #manager add MaterialExpense
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_or_no_permission_create_material_expense(self):
        url = reverse('Create_MaterialExpense')
        self.authenticate(self.waiter_user_1)
        
        response = self.client.post(url, self.test_material_expense_2, format = 'json') #waiter add MaterialExpense
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














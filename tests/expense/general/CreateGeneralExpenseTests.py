from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpGeneralExpenseTests import SetUpDataClass









class TestGeneralExpenseCreation(SetUpDataClass):
    def test_user_with_no_branch_create_general_expense(self):
        url = reverse('Create_GeneralExpense')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_general_expense_1, format = 'json') #admin add GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_general_expense(self):
        url = reverse('Create_GeneralExpense')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_general_expense_1, format = 'json') #manager add GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_or_no_permission_create_general_expense(self):
        url = reverse('Create_GeneralExpense')
        self.authenticate(self.waiter_user_1)
        
        response = self.client.post(url, self.test_general_expense_2, format = 'json') #waiter add GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














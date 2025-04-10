from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpGeneralExpenseTests import SetUpDataClass





class TestGeneralExpenseRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_general_expense(self):
        url = reverse('Get_GeneralExpense', kwargs={'pk': 2})
        self.authenticate(self.admin_user_1)

        response = self.client.get(url)                     #admin get GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_a_branch_get_general_expense(self):
        url = reverse('Get_GeneralExpense', kwargs={'pk': 1}) 
        self.authenticate(self.manager_user_1)

        response = self.client.get(url)                     #reception get GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_user_with_no_permission_get_general_expense(self):
        self.authenticate(self.waiter_user_1)
        url = reverse('Get_GeneralExpense', kwargs={'pk': 2}) 

        response = self.client.get(url)                     #waiter get GeneralExpense
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


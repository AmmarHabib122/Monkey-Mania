from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpMaterialExpenseTests import SetUpDataClass





class TestMaterialExpenseUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_material_expense(self):
        url = reverse('Update_MaterialExpense', kwargs = {'pk' : 1})
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.patch(url, self.test_material_expense_1, format = 'json') #admin update Branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_user_with_a_branch_update_material_expense(self):
        url = reverse('Update_MaterialExpense', kwargs = {'pk' : 1})

        self.authenticate(self.manager_user_1)
        response = self.client.patch(url, self.test_material_expense_1, format = 'json') #manager update MaterialExpense
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        


    def test_user_with_no_permission_update_material_expense(self):
        url = reverse('Update_MaterialExpense', kwargs = {'pk' : 1})
        self.authenticate(user = self.waiter_user_1)
    
        response = self.client.patch(url, self.test_material_expense_1, format = 'json') #waiter update Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    
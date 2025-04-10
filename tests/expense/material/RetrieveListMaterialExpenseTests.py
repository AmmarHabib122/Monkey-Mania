# from rest_framework import status
# from django.urls import reverse
# from django.utils.http import urlencode

# from base import models
# from .SetUpMaterialExpenseTests import SetUpDataClass





# class TestMaterialExpenseListRetrieve(SetUpDataClass):
#     def test_user_with_no_branch_get_all_material_expensees(self):
#         self.authenticate(self.admin_user_1)

#         resverse_url = reverse('List_MaterialExpense')       #admin get all MaterialExpense with name = material_expensee1
#         query_params = {
#             'search': 'material_expense1',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#         resverse_url = reverse('List_MaterialExpense')       #admin get all MaterialExpensees
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)




#     def test_user_with_a_branch_get_all_material_expensees(self):
#         self.authenticate(self.reception_user_1)

#         resverse_url = reverse('List_MaterialExpense')       #reception get all MaterialExpensees
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)


        

#     def test_user_with_no_permission_get_all_MaterialExpense(self):
#         self.authenticate(self.waiter_user_1)

#         resverse_url = reverse('List_MaterialExpense')       #reception get all MaterialExpensees
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


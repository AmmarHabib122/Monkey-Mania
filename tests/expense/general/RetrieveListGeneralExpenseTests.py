# from rest_framework import status
# from django.urls import reverse
# from django.utils.http import urlencode

# from base import models
# from .SetUpGeneralExpenseTests import SetUpDataClass





# class TestGeneralExpenseListRetrieve(SetUpDataClass):
#     def test_user_with_no_branch_get_all_general_expensees(self):
#         self.authenticate(self.admin_user_1)

#         resverse_url = reverse('List_GeneralExpense')       #admin get all GeneralExpense with name = general_expensee1
#         query_params = {
#             'search': 'general_expense1',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#         resverse_url = reverse('List_GeneralExpense')       #admin get all GeneralExpensees
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)




#     def test_user_with_a_branch_get_all_general_expensees(self):
#         self.authenticate(self.reception_user_1)

#         resverse_url = reverse('List_GeneralExpense')       #reception get all GeneralExpensees
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)


        

#     def test_user_with_no_permission_get_all_GeneralExpense(self):
#         self.authenticate(self.waiter_user_1)

#         resverse_url = reverse('List_GeneralExpense')       #reception get all GeneralExpensees
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


# from rest_framework import status
# from django.urls import reverse
# from django.utils.http import urlencode

# from base import models
# from .SetUpStaffSalaryTests import SetUpDataClass





# class TestStaffSalaryListRetrieve(SetUpDataClass):
#     def test_user_with_no_branch_get_all_staff_salarys(self):
#         self.authenticate(self.admin_user_1)

#         resverse_url = reverse('List_StaffSalary')       #admin get all StaffSalary with name = staff_salary1
#         query_params = {
#             'search': 'school1',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#         resverse_url = reverse('List_StaffSalary')       #admin get all StaffSalaryes
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)




#     def test_user_with_a_branch_get_all_staff_salarys(self):
#         self.authenticate(self.reception_user_1)

#         resverse_url = reverse('List_StaffSalary')       #reception get all StaffSalaryes
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)


        

#     def test_user_with_no_permission_get_all_StaffSalary(self):
#         self.authenticate(self.waiter_user_1)

#         resverse_url = reverse('List_StaffSalary')       #reception get all StaffSalaryes
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


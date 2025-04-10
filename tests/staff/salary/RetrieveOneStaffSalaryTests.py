from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffSalaryTests import SetUpDataClass





class TestStaffSalaryRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_staff_salary(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Get_StaffSalary', kwargs={'pk': 1})
        self.authenticate(self.admin_user_1)

        response = self.client.get(url)                     #admin get StaffSalary
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    



    def test_user_with_role_a_branch_get_school(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Get_StaffSalary', kwargs={'pk': 1}) 
        self.authenticate(self.manager_user_1)

        response = self.client.get(url)                     #manager get StaffSalary
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_user_with_no_permission_get_school(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.authenticate(self.waiter_user_1)
        url = reverse('Get_StaffSalary', kwargs={'pk': 1}) 

        response = self.client.get(url)                     #waiter get StaffSalary
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    


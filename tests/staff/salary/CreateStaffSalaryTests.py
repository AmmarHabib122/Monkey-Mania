from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffSalaryTests import SetUpDataClass









class TestStaffSalaryCreation(SetUpDataClass):
    def test_user_with_no_branch_create_staff_salary(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_user_with_a_branch_create_staff_salary(self):
        url = reverse('Create_StaffSalary')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #manager add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)





    def test_user_with_a_branch_or_no_permission_create_staff_salary(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(self.reception_user_1)
        
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #waiter add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    











    

    














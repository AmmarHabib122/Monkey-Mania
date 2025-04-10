from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffSalaryTests import SetUpDataClass





class TestStaffSalaryUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_staff_salary(self):
        self.authenticate(user = self.admin_user_1)
        url = reverse('Create_StaffSalary')
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_StaffSalary', kwargs = {'pk' : 1})

        self.test_staff_salary_1.pop('staff')
        response = self.client.patch(url, self.test_staff_salary_1, format = 'json') #admin update StaffSalary
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_user_with_a_branch_update_staff_salary(self):
        self.authenticate(self.manager_user_1)
        url = reverse('Create_StaffSalary')
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_StaffSalary', kwargs = {'pk' : 1})

        self.test_staff_salary_1.pop('staff')
        response = self.client.patch(url, self.test_staff_salary_1, format = 'json') #manager update StaffSalary
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        


    def test_user_with_no_permission_update_staff_salary(self):
        self.authenticate(self.manager_user_1)
        url = reverse('Create_StaffSalary')
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_StaffSalary', kwargs = {'pk' : 1})
        self.authenticate(user = self.waiter_user_1)

        self.test_staff_salary_1.pop('staff')
        response = self.client.patch(url, self.test_staff_salary_1, format = 'json') #waiter update Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    
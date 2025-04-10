from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffSalaryTests import SetUpDataClass






'''must add original_salary_minute_value to serailizer fields'''





class TestStaffSalaryFields(SetUpDataClass):
    def test_staff(self):
        ...




    def test_branch(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['branch'], self.staff1.branch.id)






    def test_original_salary_value(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['original_salary_value']), 2000)

    



    def test_original_salary_day_value(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['original_salary_day_value']), 2000 / 30)


    

    def test_original_salary_minute_value(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['original_salary_minute_value']), round(2000 / 30 / self.staff1.shift_hours / 60, 4))



    def test_over_time_value(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['over_time_value']), float(response.data['over_time']) * float(response.data['original_salary_minute_value']))




    
    def test_minus_time_value(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_2, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['minus_time_value']), round(float(response.data['minus_time']) * -1 * float(response.data['original_salary_minute_value']), 2))





    def test_delay_time_value(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_2, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['delay_time_value']), float(response.data['original_salary_day_value']) / -2)

        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['delay_time_value']), 0)
        url = reverse('Create_StaffSalary')

        self.authenticate(user = self.admin_user_1)
        self.test_staff_salary_1['delay_time'] = 91
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['delay_time_value']), float(response.data['original_salary_day_value']) / -1)






    def test_absence_days_value(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(round(float(response.data['absence_days_value']), 2), round((float(response.data['allowed_absence_days']) - float(response.data['absence_days'])) * float(response.data['original_salary_day_value']), 2))





    def test_withdraws(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(round(float(response.data['withdraws']), 2), round((self.withdraw1.value + self.withdraw2.value), 2) * -1)









    def test_fines(self):
        url = reverse('Create_StaffSalary')
        self.authenticate(user = self.admin_user_1)
        response = self.client.post(url, self.test_staff_salary_1, format = 'json') #admin add StaffSalary
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(round(float(response.data['fines']), 2), round(float(response.data['original_salary_day_value']) * (self.fine1.value + self.fine2.value), 2) * -1)







    def test_total_value(self):
        ...
    #     url = reverse('Create_StaffSalary')
    #     self.authenticate(user = self.admin_user_1)
    #     response = self.client.post(url, self.test_staff_salary_3, format = 'json') #admin add StaffSalary
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(float(response.data['total_value']), 2350)


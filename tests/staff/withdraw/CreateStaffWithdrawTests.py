from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffWithdrawTests import SetUpDataClass









class TestStaffWithdrawCreation(SetUpDataClass):
    def test_user_with_no_branch_create_staff_withdraw(self):
        url = reverse('Create_StaffWithdraw')
        self.authenticate(user = self.admin_user_1)
        
        response = self.client.post(url, self.test_staff_withdraw_1, format = 'json') #admin add StaffWithdraw
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        withdraw = models.StaffWithdraw.objects.get(pk=response.data['id'])
        self.assertEqual(withdraw.staff, self.staff1)
        self.assertEqual(withdraw.branch, self.branch_1)
        self.assertEqual(withdraw.created_by, self.admin_user_1)




    def test_user_with_a_branch_create_staff_withdraw(self):
        url = reverse('Create_StaffWithdraw')
        
        self.authenticate(user = self.manager_user_1)
        response = self.client.post(url, self.test_staff_withdraw_1, format = 'json') #manager add StaffWithdraw
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.StaffWithdraw.objects.get(pk=response.data['id']).created_by, self.manager_user_1)





    def test_user_with_a_branch_or_no_permission_create_staff_withdraw(self):
        url = reverse('Create_StaffWithdraw')
        self.authenticate(self.reception_user_1)
        
        response = self.client.post(url, self.test_staff_withdraw_2, format = 'json') #waiter add StaffWithdraw
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.StaffWithdraw.objects.count(), 2)

    











    

    














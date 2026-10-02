from django.urls import reverse
from rest_framework import status

from base import models
from .SetUpStaffWithdrawTests import SetUpDataClass


class TestStaffWithdrawFields(SetUpDataClass):
    def test_value_must_be_positive(self):
        self.authenticate(self.admin_user_1)
        payload = {**self.test_staff_withdraw_1, 'value': 0}
        response = self.client.post(reverse('Create_StaffWithdraw'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.StaffWithdraw.objects.count(), 2)

from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffFineTests import SetUpDataClass












class TestStaffFineFields(SetUpDataClass):
    def test_staff(self):
        ...




    def test_branch(self):
        ...

    


    def test_reason(self):
        ...
        



    def test_value(self):
        url = reverse('Create_StaffFine')
        self.authenticate(user = self.admin_user_1)
        
        self.test_staff_fine_1['value'] = 500
        response = self.client.post(url, self.test_staff_fine_1, format = 'json') #admin add StaffFine
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Ensure that there are no more than 2 digits before the decimal point.')

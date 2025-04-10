from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchTests import SetUpDataClass





class TestBranchUpdate(SetUpDataClass):
    def test_user_with_no_branch_update_branch(self):
        url = reverse('Update_Branch', kwargs = {'pk' : 3})
        self.authenticate(user = self.admin_user_1)
        
        self.test_branch_1['manager'] = self.manager_user_3.id
        response = self.client.patch(url, self.test_branch_1, format = 'json') #admin update Branch
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_user_with_a_branch_or_no_permission_update_branch(self):
        self.authenticate(self.manager_user_1)
        
        url = reverse('Update_Branch', kwargs = {'pk' : 3})
        self.test_branch_2['manager'] = self.manager_user_3.id
        response = self.client.patch(url, self.test_branch_2, format = 'json') #manager update Branch
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
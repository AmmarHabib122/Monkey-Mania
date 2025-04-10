from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from base import models
from .SetUpStaffTests import SetUpDataClass





class TestStaffListRetrieve(SetUpDataClass):
    def test_user_with_no_branch_get_all_staff(self):
        self.authenticate(self.admin_user_1)
        resverse_url = reverse('List_Staff')
        staff3 = models.Staff.objects.create(
            name           = "staff3",
            address        = "sdfads",
            phone_number   = '01030261332',
            salary         = 456132,
            is_active      = False,
            branch         = self.branch_2,
            created_by     = self.owner_user_1,
            allowed_absence_days  = 2, 
            shift_hours = 2, 
        )
               

        query_params = {                          #admin get all Staff with name = staff1 from all branches
            'search' : 'staff1',  
            'branch_id' : '1'
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        query_params = {                          #admin get all Staff with name = staff1 from a branch he is not in 
            'search' : 'staff1',  
            'branch_id' : '2'
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        query_params = {                          #admin get all Staff with name = staff1 from a branch  which is invlid
            'search' : 'staff1',  
            'branch_id' : '500'
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        query_params = {                          #admin get all active Staff 
            'search' : '',  
            'is_active' : "True",
            'branch_id' : '1',
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        query_params = {                          #admin get all not active Staff 
            'search' : '',  
            'is_active' : "False",
            'branch_id' : '1',
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        query_params = {                         #admin get all Staff
            'search': '',  
            'branch_id' : '1',
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)




    def test_user_with_a_branch_get_all_staff(self):
        self.authenticate(self.manager_user_1)

        resverse_url = reverse('List_Staff')       #manager get all Staffes
        query_params = {
            'search': '',  
            'branch_id' : '1',
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        

    def test_user_with_no_permission_get_all_Staff(self):
        self.authenticate(self.waiter_user_1)

        resverse_url = reverse('List_Staff')       #reception get all Staffes
        query_params = {
            'search': '',  
            'branch_id' : 'all',
        }
        query_string = urlencode(query_params, doseq=True)
        url = f"{resverse_url}?{query_string}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    


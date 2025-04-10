from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpBranchTests import SetUpDataClass












class TestBranchFields(SetUpDataClass):
    def test_name(self):
        url = reverse('Create_Branch')
        self.authenticate(self.admin_user_1)
        response = self.client.post(url, self.test_branch_1, format = 'json') 

        #test the uniqueness
        self.test_branch_2['name'] = self.test_branch_1['name']
        response = self.client.post(url, self.test_branch_2, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['message'].lower())

        #test max lenght
        self.test_branch_3['name'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_branch_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('150 characters', response.data['message'].lower())




    def test_address(self):
        url = reverse('Create_Branch')
        self.authenticate(self.admin_user_1)

        #test max lenght
        self.test_branch_3['address'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_branch_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('255 characters', response.data['message'].lower())
        



    def test_allowed_age(self):
        url = reverse('Create_Branch')
        self.authenticate(self.admin_user_1)

        #test correct age
        self.test_branch_3['allowed_age'] = -1
        response = self.client.post(url, self.test_branch_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('age can not be negative', response.data['message'].lower())




    def test_manager(self):
        url = reverse('Update_Branch', kwargs = {'pk' : 1})
        self.authenticate(self.admin_user_1)

        #test manager correct id
        data = {
            'manager' : 35
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('object does not exist', response.data['message'].lower())

        #test manager branch is assigned to other branch
        self.manager_user_6.branch = self.branch_2
        self.manager_user_6.save()
        data = {
            'manager' : 10
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You can not set a user from another branch to be the manager of this branch.', response.data['message'])

        #test manager can not be a waiter or reception
        data = {
            'manager' : 4
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You can only set a user with a manager role or higher to the branch manager field.', response.data['message'])

        
        #test manager is already a manager of another branch 
        data = {
            'manager' : 6
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You can not set a user from another branch to be the manager of this branch.', response.data['message'])





    def test_hour_prices(self):
        url = reverse('Create_Branch')
        self.authenticate(self.admin_user_1)

        #test correct children_count
        self.test_branch_3['hour_prices_set'][1]['children_count'] = 0
        response = self.client.post(url, self.test_branch_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('children-count can not be negative', response.data['message'].lower())
        self.test_branch_3['hour_prices_set'][1]['children_count'] = 10

        #test correct hour_price
        self.test_branch_3['hour_prices_set'][1]['hour_price'] = -1
        response = self.client.post(url, self.test_branch_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hour-price can not be negative', response.data['message'].lower())
        self.test_branch_3['hour_prices_set'][1]['hour_price'] = 10

        #test correct half_hour_price
        self.test_branch_3['hour_prices_set'][1]['half_hour_price'] = -1
        response = self.client.post(url, self.test_branch_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('half-hour-price can not be negative', response.data['message'].lower())
        self.test_branch_3['hour_prices_set'][1]['half_hour_price'] = 10


        #test if hour_prices is not provided
        self.test_branch_3.pop('hour_prices_set')
        response = self.client.post(url, self.test_branch_3, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('required', response.data['message'].lower())

        #test if hour_prices is null
        self.test_branch_3['hour_prices_set'] = []
        response = self.client.post(url, self.test_branch_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #test correct non-duplicate children_count
        response = self.client.post(url, self.test_branch_duplicate_4, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('each children count must be unique per branch.', response.data['message'].lower())
from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpChildTests import SetUpDataClass












class TestChildFields(SetUpDataClass):
    def test_name(self):
        url = reverse('Create_Child')
        self.authenticate(self.admin_user_1)
        response = self.client.post(url, self.test_child_1, format = 'json') 

        #test the uniqueness
        self.test_child_2['name'] = self.test_child_1['name']
        response = self.client.post(url, self.test_child_2, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['message'].lower())

        #test max lenght
        self.test_child_3['name'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('150 characters', response.data['message'].lower())




    def test_address(self):
        url = reverse('Create_Child')
        self.authenticate(self.admin_user_1)

        #test max lenght
        self.test_child_3['address'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('255 characters', response.data['message'].lower())
        
    


    def test_notes(self):
        url = reverse('Create_Child')
        self.authenticate(self.admin_user_1)

        #test max lenght
        self.test_child_3['notes'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('255 characters', response.data['message'].lower())




    def test_birth_date(self):
        url = reverse('Create_Child')
        self.authenticate(self.admin_user_1)

        #test correct age
        self.test_child_3['birth_date'] = "2026-2-6"
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Birth-Date can not be in the future.', response.data['message'])




        
    def test_special_needs(self):
        url = reverse('Update_Child', kwargs = {'pk' : 1})
        data = {
            "special_needs" : True
        }

        #test reception update special needs
        self.authenticate(self.reception_user_1)
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You Do Not have the permission to perform this action.', response.data['message'])

        #test manager update special needs
        self.authenticate(self.manager_user_1)
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_school(self):
        ...

        




    def test_child_phone_numbers_set(self):
        url = reverse('Create_Child')
        self.authenticate(self.admin_user_1)

        #test duplicate phone numbers 
        self.test_child_3['child_phone_numbers_set'][0]['phone_number']['value'] = "11111112222"
        self.test_child_3['child_phone_numbers_set'][1]['phone_number']['value'] = "11111112222"
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Each Phone-number must be unique per child.', response.data['message'])

        #test phone number lenght
        self.test_child_3['child_phone_numbers_set'][0]['phone_number']['value'] = "111222"
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Phone number must be exactly 11 digits long.', response.data['message'])

        #test phone number is digigt
        self.test_child_3['child_phone_numbers_set'][0]['phone_number']['value'] = "1265324521a"
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Phone number must contain only digits.', response.data['message'])

        #test reltion ship is in allowed values
        self.test_child_3['child_phone_numbers_set'][0]['phone_number']['value'] = "12653245210"
        self.test_child_3['child_phone_numbers_set'][0]['relationship'] = "motherer"
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Allowed values: father, mother, sibling, other.', response.data['message'])

        #test child_phone_numbers_set is null
        self.test_child_3.pop('child_phone_numbers_set')
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The field 'child_phone_numbers_set' is required.", response.data['message'])

        #test child_phone_numbers_set is [] in create
        self.test_child_3['child_phone_numbers_set'] = []
        response = self.client.post(url, self.test_child_3, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Child Phone Numbers must be provided.', response.data['message'])

        #test child_phone_numbers_set is [] in update
        url = reverse('Update_Child', kwargs = {'pk' : 2})
        response = self.client.patch(url, self.test_child_2, format = 'json') 
        data = {
            'child_phone_numbers_set' : []
        }
        response = self.client.patch(url, data, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['child_phone_numbers_set'], [])

        
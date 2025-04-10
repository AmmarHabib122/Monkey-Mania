from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpDiscountTests import SetUpDataClass












class TestDiscountFields(SetUpDataClass):
    def test_name(self):
        ...




    def test_address(self):
        ...

    


    def test_type(self):
        url = reverse('Create_Discount')
        self.authenticate(self.admin_user_1)

        #test type allowed values
        self.test_discount_2['type'] = "sadf"
        response = self.client.post(url, self.test_discount_2, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Discount allowed types are ['percentage', 'fixed', 'new value'].", response.data['message'])


    def test_branch(self):
        url = reverse('Create_Discount')
        self.authenticate(self.admin_user_1)

        #test duplicate ids
        self.test_discount_2['branches'].append(1)
        response = self.client.post(url, self.test_discount_2, format = 'json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You tried to add the same branch more than once', response.data['message'])


    # def test_notes(self):
    #     url = reverse('Create_Discount')
    #     self.authenticate(self.admin_user_1)

    #     #test max lenght
    #     self.test_discount_2['notes'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
    #     response = self.client.post(url, self.test_discount_2, format = 'json') 
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('255 characters', response.data['message'].lower())
        



    
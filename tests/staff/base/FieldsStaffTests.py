from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpStaffTests import SetUpDataClass












class TestStaffFields(SetUpDataClass):
    def test_name(self):
        url = reverse('Create_Staff')
        self.authenticate(self.admin_user_1)
        response = self.client.post(url, self.test_staff_1, format = 'multipart') 

        #test the uniqueness
        self.test_staff_2['name'] = self.test_staff_1['name']
        response = self.client.post(url, self.test_staff_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('staff with this name already exists.', response.data['message'].lower())

        #test max lenght
        self.test_staff_2['name'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_staff_2, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('150 characters', response.data['message'].lower())




    def test_address(self):
        url = reverse('Create_Staff')
        self.authenticate(self.admin_user_1)

        #test max lenght
        self.test_staff_3['address'] = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        response = self.client.post(url, self.test_staff_3, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('255 characters', response.data['message'].lower())

    


    def test_phone_number(self):
        ...
    


    def test_day_value(self):
        url = reverse('Create_Staff')
        self.authenticate(self.admin_user_1)

        response = self.client.post(url, self.test_staff_3, format = 'multipart') 
        self.assertEqual(66.67, float(response.data['day_value']))




    def test_salary(self):
        url = reverse('Create_Staff')
        self.authenticate(self.admin_user_1)

        self.test_staff_3['salary'] = -1
        response = self.client.post(url, self.test_staff_3, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Salary can not be negative or equal to zero.', response.data['message'])
        
        self.test_staff_3['salary'] = 0
        response = self.client.post(url, self.test_staff_3, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Salary can not be negative or equal to zero.', response.data['message'])
        
        self.test_staff_3['salary'] = 'dfsa'
        response = self.client.post(url, self.test_staff_3, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('a valid number is required.', response.data['message'].lower())

        self.test_staff_3.pop('salary', None)
        response = self.client.post(url, self.test_staff_3, format = 'multipart') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('required', response.data['message'].lower())


    

    def test_branch(self):
        ...




    def test_images(self):
        url = reverse('Create_Staff')
        self.authenticate(user = self.admin_user_1)
        
        self.test_staff_1['images'] = [
            self.image1,
            self.image7large
        ]
        response = self.client.post(url, self.test_staff_1, format = 'multipart')    #admin add staff wih large image
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Image file is too large! Max size allowed', response.data['message'])

        self.test_staff_1.pop('images', None)
        response = self.client.post(url, self.test_staff_1, format = 'multipart')    #admin add staff wih null images
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_staff_2['images'] = []
        response = self.client.post(url, self.test_staff_2, format = 'multipart')    #admin add staff wih empty images
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('Update_Staff', kwargs = {'pk' : 3})

        branch3 = self.test_staff_3.pop('branch', None)
        response = self.client.patch(url, self.test_staff_3, format = 'multipart')  #admin add photos
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['images']), 3)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);

        # self.test_staff_3['branch'] = branch3
        self.test_staff_3['images'] = self.image5
        response = self.client.patch(url, self.test_staff_3, format = 'multipart')  #admin delete 2 photos
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['images']), 1)

        self.test_staff_3['images'] = []
        response = self.client.patch(url, self.test_staff_3, format = 'multipart')  #admin delete all photos
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['images']), 0)
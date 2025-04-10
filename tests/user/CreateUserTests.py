from rest_framework import status
from django.urls import reverse

from base import models
from .SetUpUserTests import SetUpDataClass









class TestUserCreation(SetUpDataClass):

    def test_user_with_no_branch_create_user(self):
        url = reverse('Create_User')
        self.authenticate(self.admin_user_1)
        
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') #admin add waiter
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);

        response = self.client.post(url, self.test_reception_user_2, format = 'multipart') #admin add reception
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);


        response = self.client.post(url, self.test_manager_user_2, format = 'multipart') #admin add a manager
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);


        response = self.client.post(url, self.test_admin_user_2, format = 'multipart') #admin add an admin
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);


        response = self.client.post(url, self.test_owner_user_2, format = 'multipart') #admin add an owner
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        



    def test_user_with_a_branch_create_user(self):
        
        url = reverse('Create_User')
        self.authenticate(self.manager_user_1)
        
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart')
        self.assertEqual(self.manager_user_1.branch.id, response.data["branch"]) #manager add waiter
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);
        
        response = self.client.post(url, self.test_reception_user_2, format = 'multipart') #manager add reception
        self.assertEqual(self.manager_user_1.branch.id, response.data["branch"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);

        response = self.client.post(url, self.test_manager_user_2, format = 'multipart') #manager add a manager
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);

        response = self.client.post(url, self.test_admin_user_2, format = 'multipart') #manager add an admin
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.image1.seek(0); self.image2.seek(0); self.image3.seek(0); self.image4.seek(0); self.image5.seek(0); self.image6.seek(0);

        response = self.client.post(url, self.test_owner_user_2, format = 'multipart') #manager add an owner
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_user_with_no_permission_create_user(self):
        url = reverse('Create_User')
        self.authenticate(self.reception_user_1)
        
        response = self.client.post(url, self.test_waiter_user_2, format = 'multipart') #reception add waiter
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)






    

    














    # def test_user_username(self):
    #     url = reverse('Create_User')
    #     self.authenticate(self.admin_user_1)
    #     response = self.client.post(url, self.test_waiter_user_2, format = 'multipart')

    #     self.test_reception_user_2['username'] = self.test_waiter_user_2['username']
    #     response = self.client.post(url, self.test_reception_user_2, format = 'multipart') 
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     with self.assertRaises(IntegrityError):
    #         response

from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import os

from base import models




class SetUpDataClass(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        #branch 1
        cls.owner_user_1   = models.User.objects.create(    #1
            username       = "UserOwner1",
            phone_number   = "11111111111",
            password       = "123456789Ah",
            role           = "owner",
        )
        cls.admin_user_1  = models.User.objects.create(     #2
            username      = "UserAdmin1",
            phone_number  = "22222222222",
            password      = "123456789Ah",
            role          = "admin",
        )
        cls.manager_user_1 = models.User.objects.create(    #3
            username       = "UserManager1",
            phone_number   = "33333333333",
            password       = "123456789Ah",
            role           = "manager",
        )
        cls.reception_user_1 = models.User.objects.create(  #4
            username         = "UserReception1",
            phone_number     = "44444444444",
            password         = "123456789Ah",
            role             = "reception",
        )
        cls.waiter_user_1 = models.User.objects.create(     #5
            username      = "UserWaiter1",
            phone_number  = "55555555555",
            password      = "123456789Ah",
            role          = "waiter",
        )
        cls.branch_1    = models.Branch.objects.create(    
            name        = 'Branch1',
            address     = 'new_damietta savana',
            indoor      = False,
            allowed_age = 5,
            manager     = cls.manager_user_1,
            created_by  = cls.admin_user_1,
            delay_allowed_time  = 60,
            delay_fine_interval = 30,
            delay_fine_value    = 0.5,
        )
        
        cls.manager_user_1.branch   = cls.branch_1
        cls.reception_user_1.branch = cls.branch_1
        cls.waiter_user_1.branch    = cls.branch_1
        cls.manager_user_1.save()
        cls.reception_user_1.save()
        cls.waiter_user_1.save()


        #branch 2
        cls.owner_user_2   = models.User.objects.create(    #6
            username       = "UserOwner2",
            phone_number   = "11111111112",
            password       = "123456789Ah",
            role           = "owner",
        )
        cls.admin_user_2  = models.User.objects.create(     #7
            username      = "UserAdmin2",
            phone_number  = "22222222223",
            password      = "123456789Ah",
            role          = "admin",
        )
        cls.manager_user_2 = models.User.objects.create(    #8
            username       = "UserManager2",
            phone_number   = "33333333332",
            password       = "123456789Ah",
            role           = "manager",
        )
        cls.reception_user_2 = models.User.objects.create(  #9
            username         = "UserReception2",
            phone_number     = "44444444442",
            password         = "123456789Ah",
            role             = "reception",
        )
        cls.waiter_user_2 = models.User.objects.create(     #10
            username      = "UserWaiter2",
            phone_number  = "55555555552",
            password      = "123456789Ah",
            role          = "waiter",
        )
        cls.branch_2    = models.Branch.objects.create(
            name        = 'Branch2',
            address     = 'new_damietta savana',
            indoor      = False,
            allowed_age = 5,
            manager     = cls.manager_user_2,
            created_by  = cls.admin_user_1,
            delay_allowed_time  = 60,
            delay_fine_interval = 30,
            delay_fine_value    = 0.5,
        )
        
        cls.manager_user_2.branch   = cls.branch_2
        cls.reception_user_2.branch = cls.branch_2
        cls.waiter_user_2.branch    = cls.branch_2
        cls.manager_user_2.save()
        cls.reception_user_2.save()
        cls.waiter_user_2.save()


        base_dir     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_folder = "_media_for_testing_"
        def get_uploaded_file(filename):
            file_path = os.path.join(base_dir, image_folder, filename)
            with open(file_path, "rb") as f:
                return SimpleUploadedFile(
                    name=filename,
                    content=f.read(),
                    content_type="image/png"
                )
        cls.image1 = get_uploaded_file("test1.png")
        cls.image2 = get_uploaded_file("test2.png")
        cls.image3 = get_uploaded_file("test3.png")
        cls.image4 = get_uploaded_file("test4.png")
        cls.image5 = get_uploaded_file("test5.png")
        cls.image6 = get_uploaded_file("test6.png")
        
        

        cls.test_waiter_user_2 = {
            'username': 'newwaiter',
            'phone_number': '17534682951',
            'password': 'sadflkjAh',
            'confirm_password': 'sadflkjAh',
            'role': 'waiter',
            'branch': 2,
            'staff_name' : 'newwaiter',
            'staff_address' : 'newwaiter',
            'staff_shift_hours' : 5,
            'staff_allowed_absence_days' : 2,
            'staff_salary' : 651465,
            'staff_images' : cls.image1,

        }
        cls.test_reception_user_2 = {
            'username': 'newreception',
            'phone_number': '17504682951',
            'password': 'sadflkjAh',
            'confirm_password': 'sadflkjAh',
            'role': 'reception',
            'branch': 2,
            'staff_name' : 'newreception',
            'staff_address' : 'newwaiter',
            'staff_shift_hours' : 5,
            'staff_salary' : 651465,
            'staff_allowed_absence_days' : 2,
            'staff_images' : [
                cls.image2
            ],
        }
        cls.test_manager_user_2 = {
            'username': 'newmanager',
            'phone_number': '17537682951',
            'password': 'sadflkjAh',
            'confirm_password': 'sadflkjAh',
            'role': 'manager',
            'branch': 2,
            'staff_name' : 'newmanager',
            'staff_address' : 'newwaiter',
            'staff_shift_hours' : 5,
            'staff_allowed_absence_days' : 2,
            'staff_salary' : 651465,
            'staff_images' : [
                cls.image1,
                cls.image4,
                cls.image5
            ],
        }
        cls.test_admin_user_2 = {
            'username': 'newadmin',
            'phone_number': '17537682351',
            'password': '123456Ah',
            'confirm_password': '123456Ah',
            'role': 'admin',
            'branch': 2,
            'staff_name' : 'newadmin',
            'staff_address' : 'newwaiter',
            'staff_allowed_absence_days' : 2,
            'staff_shift_hours' : 5,
            'staff_salary' : 651465,
            'staff_images' : [
                cls.image6,
                cls.image1,
                cls.image2
            ],
        }
        cls.test_owner_user_2 = {
            'username': 'newowner',
            'phone_number': '17527682951',
            'password': '123456Ah',
            'confirm_password': '123456Ah',
            'role': 'owner',
            'branch': 2,
            'staff_name' : 'newowner',
            'staff_address' : 'newwaiter',
            'staff_allowed_absence_days' : 2,
            'staff_shift_hours' : 5,
            'staff_salary' : 651465,
            'staff_images' : [
                cls.image1,
                cls.image2,
                cls.image3
            ],
        }

        


    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
    

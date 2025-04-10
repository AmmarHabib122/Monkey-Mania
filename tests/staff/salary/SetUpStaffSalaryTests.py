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
            name                = 'Branch1',
            address             = 'new_damietta savana',
            indoor              = False,
            allowed_age         = 5,
            manager             = cls.manager_user_1,
            created_by          = cls.admin_user_1,
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
            username            = "UserWaiter2",
            phone_number        = "55555555552",
            password            = "123456789Ah",
            role                = "waiter",
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


        base_dir     = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_folder = "_media_for_testing_"
        def upload_png(filename):
            file_path = os.path.join(base_dir, image_folder, filename)
            with open(file_path, "rb") as f:
                return SimpleUploadedFile(
                    name=filename,
                    content=f.read(),
                    content_type="image/png"
                )
        def upload_jpg(filename):
            file_path = os.path.join(base_dir, image_folder, filename)
            with open(file_path, "rb") as f:
                return SimpleUploadedFile(
                    name=filename,
                    content=f.read(),
                    content_type="image/jpg"
                )
        cls.image1      = upload_png("test1.png")
        cls.image2      = upload_png("test2.png")
        cls.image3      = upload_png("test3.png")
        cls.image4      = upload_png("test4.png")
        cls.image5      = upload_png("test5.png")
        cls.image6      = upload_png("test6.png")
        cls.image7large = upload_jpg("test7large.jpg")

        cls.staff1 = models.Staff.objects.create(
            name           = "staff1",
            address        = "sdfads",
            phone_number   = '01030261398',
            salary         = 2000,
            branch         = cls.branch_1,
            created_by     = cls.owner_user_1,
            allowed_absence_days = 2,
            shift_hours   = 5,
        )
        cls.staff2 = models.Staff.objects.create(
            name           = "staff2",
            address        = "sdfads",
            phone_number   = '01030261390',
            salary         = 3600,
            branch         = cls.branch_2,
            created_by     = cls.owner_user_1,
            allowed_absence_days = 2,
            shift_hours   = 4,
        )
        cls.withdraw1 = models.StaffWithdraw.objects.create(
            staff      = cls.staff1,
            branch     = cls.branch_1,
            value      = 500,
            created_by = cls.owner_user_1,
        )
        cls.withdraw2 = models.StaffWithdraw.objects.create(
            staff      = cls.staff1,
            branch     = cls.branch_1,
            value      = 600,
            created_by = cls.owner_user_1,
        )
        cls.withdraw3 = models.StaffWithdraw.objects.create(
            staff      = cls.staff2,
            branch     = cls.branch_2,
            value      = 400,
            created_by = cls.owner_user_1,
        )

        cls.fine1 = models.StaffFine.objects.create(
            staff      = cls.staff1,
            branch     = cls.branch_1,
            reason     = 'sad;f',
            value      = 1,
            created_by = cls.owner_user_1,
        )
        cls.fine2 = models.StaffFine.objects.create(
            staff       = cls.staff1,
            branch      = cls.branch_1,
            reason      = 'sad;f',
            value       = 1.5,
            created_by  = cls.owner_user_1,
        )
        cls.test_staff_salary_1 = {
            "staff"        : 1,
            "delay_time"   : 59,
            "minus_time"   : 0,
            "over_time"    : 90,
            "absence_days" : 15,
            "bonus_value"  : 100,
        }
        cls.test_staff_salary_2 = {
            "staff"        : 1,
            "delay_time"   : 65,
            "minus_time"   : 50,
            "over_time"    : 150,
            "absence_days" : 11,
            "bonus_value"  : 1000,
        }
        cls.test_staff_salary_3 = {
            "staff"        : 2,
            "delay_time"   : 59,
            "minus_time"   : 630,
            "over_time"    : 2921,
            "absence_days" : 3,
            "bonus_value"  : 300,
        }

        


    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

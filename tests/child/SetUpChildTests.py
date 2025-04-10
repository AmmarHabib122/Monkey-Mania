from django.test import TestCase
from rest_framework.test import APIClient

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
        cls.manager_user_2 = models.User.objects.create(    #6
            username       = "UserManager2",
            phone_number   = "33333333332",
            password       = "123456789Ah",
            role           = "manager",
        )


        cls.branch_1    = models.Branch.objects.create(    
            name        = 'Branch1',
            address    = 'new_damietta savana',
            indoor      = False,
            allowed_age = 5,
            manager     = cls.manager_user_1,
            created_by  = cls.admin_user_1,
            delay_allowed_time  = 60,
            delay_fine_interval = 30,
            delay_fine_value    = 0.5,
        )
        cls.branch_2    = models.Branch.objects.create(    
            name        = 'Branch2',
            address    = 'new_damietta markaiz',
            indoor      = False,
            allowed_age = 5,
            manager     = cls.manager_user_2,
            created_by  = cls.admin_user_1,
            delay_allowed_time  = 60,
            delay_fine_interval = 30,
            delay_fine_value    = 0.5,
        )
        cls.manager_user_1.branch   = cls.branch_1
        cls.manager_user_2.branch   = cls.branch_2
        cls.reception_user_1.branch = cls.branch_1
        cls.waiter_user_1.branch    = cls.branch_1
        cls.manager_user_1.save()
        cls.manager_user_2.save()
        cls.reception_user_1.save()
        cls.waiter_user_1.save()

        cls.school_1 = models.School.objects.create(
            name = 'school1',
            address = 'new_damietta markaizas',
            notes = 'special needs',
            created_by = cls.manager_user_1
        )
        cls.school_2 = models.School.objects.create(
            name = 'school2',
            address = 'new_damietta markaizas',
            notes = 'special needs',
            created_by = cls.manager_user_1
        )

        cls.child_1 = models.Child.objects.create(
            name = 'child1',
            birth_date = '2023-5-30',
            address = 'new_damietta markaizas',
            notes = 'special needs',
            created_by = cls.manager_user_1,
        )
        cls.child_2 = models.Child.objects.create(
            name = 'child2',
            birth_date = '2023-5-30',
            address = 'new_damietta markaizas',
            notes = 'special needs',
            created_by = cls.manager_user_1,
        )
        cls.test_child_1 = {
            "name"            : "testchild1",
            "birth_date"      : "2024-5-30",
            "address"         : "new_damietta markaizas",
            "notes"           : "special needs",
            "school"          : cls.school_1.id,
            "child_phone_numbers_set" : [
                {
                    "phone_number" : {"value" : "12345678912"},
                    "relationship" : "other"
                },
                {
                    "phone_number" : {"value" : "12345670912"},
                    "relationship" : "other"
                },
            ],
        }
        cls.test_child_2 = {
            "name"            : 'testchild2',
            "birth_date"      : '2024-5-30',
            "address"         : 'new_damietta markaizas',
            "notes"           : 'special needs',
            "school"          : cls.school_2.id,
            'child_phone_numbers_set' : [
                {
                    'phone_number' : {'value' : '12335678912'},
                    'relationship' : 'sibling'
                },
                {
                    'phone_number' : {'value' : '12355670912'},
                    'relationship' : 'mother'
                },
            ],
        }
        cls.test_child_3 = {
            "name"            : 'testchild3',
            "birth_date"      : '2024-5-30',
            "address"         : 'new_damietta markaizas',
            "notes"           : 'special needs',
            "school"          : cls.school_1.id,
            'child_phone_numbers_set' : [
                {
                    'phone_number' : {'value' : '12345678910'},
                    'relationship' : 'father'
                },
                {
                    'phone_number' : {'value' : '12845670912'},
                    'relationship' : 'mother'
                },
            ],
        }
        

        


    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
    

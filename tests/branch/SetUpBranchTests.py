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
        cls.manager_user_3 = models.User.objects.create(    #7
            username       = "UserManager3",
            phone_number   = "33333333322",
            password       = "123456789Ah",
            role           = "manager",
        )
        cls.manager_user_4 = models.User.objects.create(    #8
            username       = "UserManager4",
            phone_number   = "34333333332",
            password       = "123456789Ah",
            role           = "manager",
        )
        cls.manager_user_5 = models.User.objects.create(    #9
            username       = "UserManager5",
            phone_number   = "33334333322",
            password       = "123456789Ah",
            role           = "manager",
        )
        cls.manager_user_6 = models.User.objects.create(    #10
            username       = "UserManager6",
            phone_number   = "33334336322",
            password       = "123456789Ah",
            role           = "manager",
        )
        cls.manager_user_7 = models.User.objects.create(    #11
            username       = "UserManager7",
            phone_number   = "33334336372",
            password       = "123456789Ah",
            role           = "manager",
        )


        cls.branch_1 = models.Branch.objects.create(    
            name                 = 'Branch1',
            address              = 'new_damietta savana',
            indoor               = False,
            allowed_age          = 5,
            manager              = cls.manager_user_1,
            created_by           = cls.admin_user_1,
            delay_allowed_time   = 45,
            delay_fine_interval  = 30,
            delay_fine_value     = 0.5,
        )
        cls.branch_2 = models.Branch.objects.create(    
            name                 = 'Branch2',
            address              = 'new_damietta markaiz',
            indoor               = False,
            allowed_age          = 5,
            manager              = cls.manager_user_2,
            created_by           = cls.admin_user_1,
            delay_allowed_time   = 45,
            delay_fine_interval  = 30,
            delay_fine_value     = 0.5,
        )
        cls.branch_3 = models.Branch.objects.create(    
            name                 = 'Branch3',
            address              = 'new_damietta markaiz',
            indoor               = False,
            allowed_age          = 5,
            manager              = cls.manager_user_3,
            created_by           = cls.admin_user_1,
            delay_allowed_time   = 45,
            delay_fine_interval  = 30,
            delay_fine_value     = 0.5,
        )
        cls.manager_user_1.branch   = cls.branch_1
        cls.manager_user_2.branch   = cls.branch_2
        cls.manager_user_3.branch   = cls.branch_3
        cls.reception_user_1.branch = cls.branch_1
        cls.waiter_user_1.branch    = cls.branch_1
        cls.manager_user_1.save()
        cls.manager_user_2.save()
        cls.manager_user_3.save()
        cls.reception_user_1.save()
        cls.waiter_user_1.save()


        cls.test_branch_1 = {
            "name"                   : 'TestBranch1',
            "address"                : 'new_damietta markaizas',
            "indoor"                 : False,
            "allowed_age"            : 5,         
            "delay_allowed_time"     : 45,
            "delay_fine_interval"    : 30,
            "delay_fine_value"       : 0.5,
            "manager"                : cls.manager_user_4.id,
            'hour_prices_set' : [
                {
                    'children_count'  : 1,
                    'hour_price'      : 70,
                    'half_hour_price' : 40,
                },
                {
                    'children_count'  : 2,
                    'hour_price'      : 120,
                    'half_hour_price' : 70,
                }
            ],
        }
        cls.test_branch_2 = {
            "name"                   : 'TestBranch2',
            "address"                : 'new_damietta msdfarkaizas',
            "indoor"                 : False,
            "allowed_age"            : 3,
            "delay_allowed_time"     : 45,
            "delay_fine_interval"    : 30,
            "delay_fine_value"       : 0.5,
            "manager"                : cls.manager_user_5.id,
            'hour_prices_set' : [
                {
                    'children_count'  : 1,
                    'hour_price'      : 500,
                    'half_hour_price' : 600,
                },
                {
                    'children_count'  : 2,
                    'hour_price'      : 700,
                    'half_hour_price' : 800,
                },
                {
                    'children_count'  : 3,
                    'hour_price'      : 123,
                    'half_hour_price' : 124,
                },
                {
                    'children_count'  : 4,
                    'hour_price'      : 125,
                    'half_hour_price' : 126,
                }
            ]
        }
        cls.test_branch_3 = {
            "name"                   : 'TestBrakhjgnch3',
            "address"                : 'new_damietta msdfarkaizas',
            "indoor"                 : False,
            "allowed_age"            : 3,
            "delay_allowed_time"     : 45,
            "delay_fine_interval"    : 30,
            "delay_fine_value"       : 0.5,
            "manager"                : cls.manager_user_6.id,
            'hour_prices_set' : [
                {
                    'children_count'  : 1,
                    'hour_price'      : 70,
                    'half_hour_price' : 40,
                },
                {
                    'children_count'  : 2,
                    'hour_price'      : 120,
                    'half_hour_price' : 70,
                }
            ]
        }
        cls.test_branch_duplicate_4 = {
            "name"                   : 'TestBranch4',
            "address"                : 'new_damietta msdfarkaizas',
            "indoor"                 : False,
            "allowed_age"            : 3,
            "delay_allowed_time"     : 45,
            "delay_fine_interval"    : 30,
            "delay_fine_value"       : 0.5,
            "manager"                : cls.manager_user_7.id,
            'hour_prices_set' : [
                {
                    'children_count'  : 1,
                    'hour_price'      : 70,
                    'half_hour_price' : 40,
                },
                {
                    'children_count'  : 2,
                    'hour_price'      : 120,
                    'half_hour_price' : 70,
                },
                {
                    'children_count'  : 1,
                    'hour_price'      : 12,
                    'half_hour_price' : 7,
                }
            ]
        }

        


    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
    

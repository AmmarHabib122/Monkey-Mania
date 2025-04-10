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
        cls.child_3 = models.Child.objects.create(
            name = 'child3',
            birth_date = '2023-5-30',
            address = 'new_damietta markaizas',
            notes = 'special needs',
            created_by = cls.manager_user_1,
        )
        cls.child_4 = models.Child.objects.create(
            name = 'child4',
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
        
        cls.subscription_1 = models.Subscription.objects.create(
            name              = 'subscription1',
            hours             = 15,
            instance_duration = 30,
            price             = 150,
            created_by        = cls.admin_user_1,
            # usable_in_branches    = [
            # ],
            # creatable_in_branches = [
            #     1,
            #     2,
            # ],
        )
        cls.subscription_1.creatable_in_branches.add(cls.branch_1, cls.branch_2)
        cls.subscription_1.save()
        cls.subscription_2 = models.Subscription.objects.create(
            name              = 'subscription2',
            hours             = 15,
            instance_duration = 30,
            price             = 150,
            created_by        = cls.admin_user_1,
            # usable_in_branches    = [
            #     1
            # ],
            # creatable_in_branches = [
            #     2,
            # ],
        )
        cls.subscription_2.usable_in_branches.add(cls.branch_1)
        cls.subscription_2.creatable_in_branches.add(cls.branch_2)
        cls.subscription_2.save()

        cls.subscription_instance_1 = models.SubscriptionInstance.objects.create(
            cash              = 50,
            visa              = 50,
            instapay          = 50,
            price             = 150,
            hours             = 15,
            subscription      = cls.subscription_1,
            child             = cls.child_1,
            branch            = cls.branch_1,
            expire_date       = '2026-5-3',
            created_by        = cls.admin_user_1,
        )
        cls.subscription_instance_2 = models.SubscriptionInstance.objects.create(
            cash              = 50,
            visa              = 50,
            instapay          = 50,
            price             = 150,
            hours             = 15,
            subscription      = cls.subscription_2,
            child             = cls.child_2,
            branch            = cls.branch_1,
            expire_date       = '2026-5-3',
            created_by        = cls.admin_user_1,
        )

        cls.test_subscription_instance_1 = {
            "cash"              : 50,
            "visa"              : 50,
            "instapay"          : 50,
            "subscription"      : 1,
            "child"             : 3,
            "branch"            : 1,
        }
        cls.test_subscription_instance_2 = {
            "cash"              : 50,
            "visa"              : 50,
            "instapay"          : 50,
            "subscription"      : 2,
            "child"             : 4,
            "branch"            : 2,
        }

        


    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
    

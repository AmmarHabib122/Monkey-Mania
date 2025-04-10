from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


from base import models




class SetUpDataClass(TestCase):
    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
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
        cls.branch_2    = models.Branch.objects.create(    
            name        = 'Branch2',
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

        cls.client.force_authenticate(user = cls.admin_user_1)

        cls.product_1 = models.Product.objects.create(
            layer1      = 'dessert', 
            layer2      = 'waffle', 
            layer3      = 'nutella', 
            created_by  = cls.admin_user_1, 
        )
        cls.product_2 = models.Product.objects.create(
            layer1      = 'dessert', 
            layer2      = 'waffle', 
            layer3      = 'pistachio', 
            created_by  = cls.admin_user_1, 
        )
        cls.product_3 = models.Product.objects.create(
            layer1      = 'dessert', 
            layer2      = 'tajin', 
            layer3      = 'pistachio', 
            created_by  = cls.admin_user_1, 
        )

        cls.material_1 = models.Material.objects.create(
            name          = 'nutella',
            measure_unit  = 'kilo',
            created_by    = cls.admin_user_1,
        )
        cls.material_2 = models.Material.objects.create(
            name          = 'lotus',
            measure_unit  = 'kilo',
            created_by    = cls.admin_user_1
        )
        cls.branch_material_1 = models.BranchMaterial.objects.create(
            material          = cls.material_1,
            branch            = cls.branch_1,
            available_units   = 15,      
            created_by        = cls.admin_user_1
        )
        cls.branch_material_2 = models.BranchMaterial.objects.create(
            material          = cls.material_2,
            branch            = cls.branch_1,
            available_units   = 10,
            created_by        = cls.admin_user_1
        )
        
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
        cls.child_5 = models.Child.objects.create(
            name = 'child5',
            birth_date = '2023-5-30',
            address = 'new_damietta markaizas',
            notes = 'special needs',
            created_by = cls.manager_user_1,
        )
        hour_prices_data_1 = [
            models.HourPrice(
                children_count   = 1,
                hour_price       = 70,
                half_hour_price  = 40,
                branch           = cls.branch_1,
            ),
            models.HourPrice(
                children_count   = 2,
                hour_price       = 120,
                half_hour_price  = 70,
                branch           = cls.branch_1,
            ),
            models.HourPrice(
                children_count   = 3,
                hour_price       = 170,
                half_hour_price  = 100,
                branch           = cls.branch_1,
            ),
            models.HourPrice(
                children_count   = 4,
                hour_price       = 210,
                half_hour_price  = 120,
                branch           = cls.branch_1,
            ),
            models.HourPrice(
                children_count   = 5,
                hour_price       = 250,
                half_hour_price  = 150,
                branch           = cls.branch_1,
            ),
        ]
        models.HourPrice.objects.bulk_create(hour_prices_data_1)

        branch_product_1 = {
            "product"        : 1,
            "branch"         : 1,
            "warning_units"  : 150,
            "price"          : 100,
            "material_consumptions_set" : [
                {
                    'material' : 1,
                    'consumption' : 0.1,
                },
                {
                    'material' : 2,
                    'consumption' : 0.1,
                }
            ]
        }
        branch_product_2 = {
            "product"        : 3,
            "branch"         : 1,
            "warning_units"  : 5,
            "price"          : 150,
            "material_consumptions_set" : [
                {
                    'material' : 1,
                    'consumption' : 0.2,
                },
                {
                    'material' : 2,
                    'consumption' : 0.2,
                }
            ]
        }
        
        url = reverse('Create_BranchProduct')
        response = cls.client.post(url, branch_product_1, format = 'json') 
        assert response.status_code == status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}"
        response = cls.client.post(url, branch_product_2, format = 'json') 
        assert response.status_code == status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}"

        bill_1 = {
            "children" : [
                1,
                2,
            ],
            'branch' : 1,
        }
        bill_duplicate = {
            "children" : [
                1,
                2,
            ],
            'branch' : 2,
        }
        bill_2 = {
            "children" : [
                3,
                4,
                5,
            ],
            'branch' : 1,
        }
        url = reverse('Create_Bill')
        response = cls.client.post(url, bill_1, format = 'json') 
        assert response.status_code == status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}"
        response = cls.client.post(url, bill_2, format = 'json') 
        assert response.status_code == status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}"

        cls.offer_1 = models.Offer.objects.create(
            name       = 'offer1',
            created_by = cls.admin_user_1,
        )
        cls.offer_2 = models.Offer.objects.create(
            name       = 'offer2',
            created_by = cls.admin_user_1,
        )
        cls.offer_3 = models.Offer.objects.create(
            name       = 'offer3',
            created_by = cls.admin_user_1,
        )

        branch_offer_1 = {
            'offer' : 3,
            'branch' : 1,
            'price' : 300,
            'expire_date' : '2026-5-3',
            'products_set' : [
                {
                    'product' : 1,
                    'quantity' : 2,
                },
                {
                    'product' : 2,
                    'quantity' : 1,
                },
            ]
        }

        url = reverse('Create_BranchOffer')
        response = cls.client.post(url, branch_offer_1, format = 'json') 
        assert response.status_code == status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}"
        
        cls.test_branch_offer_1 = {
            'offer' : 1,
            'branch' : 1,
            'price' : 300,
            'expire_date' : '2026-5-3',
            'products_set' : [
                {
                    'product' : 1,
                    'quantity' : 2,
                },
                {
                    'product' : 2,
                    'quantity' : 1,
                },
            ]
        }
        cls.test_branch_offer_2 = {
            'offer' : 2,
            'branch' : 1,
            'price' : 200,
            'expire_date' : '2026-5-3',
            'products_set' : [
                {
                    'product' : 1,
                    'quantity' : 1,
                },
                {
                    'product' : 2,
                    'quantity' : 2,
                },
            ]
        }

    
    

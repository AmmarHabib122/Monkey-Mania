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
        cls.branch_product_1 = models.BranchProduct.objects.create(
            product       = cls.product_1, 
            branch        = cls.branch_2, 
            warning_units = 5, 
            price         = 6514,
            created_by    = cls.admin_user_1, 
        )
        cls.branch_product_2 = models.BranchProduct.objects.create(
            product       = cls.product_2, 
            branch        = cls.branch_1, 
            warning_units = 5, 
            price         = 6514,
            created_by    = cls.admin_user_1, 
        )
        cls.branch_product_3 = models.BranchProduct.objects.create(
            product       = cls.product_3, 
            branch        = cls.branch_1, 
            warning_units = 5, 
            price         = 6514,
            created_by    = cls.admin_user_1, 
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
        cls.branch_material_3 = models.BranchMaterial.objects.create(
            material          = cls.material_1,
            branch            = cls.branch_2,
            available_units   = 20,
            created_by        = cls.admin_user_1
        )

        cls.test_branch_product_1 = {
            "product"        : 1,
            "branch"         : 1,
            "warning_units"  : 150,
            "price"          : 231,
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
        cls.test_branch_product_2 = {
            "product"        : 3,
            "branch"         : 1,
            "warning_units"  : 5,
            "price"          : 231,
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
        cls.test_branch_product_3 = {
            "product"        : 3,
            "branch"         : 1,
            "warning_units"  : 5,
            "price"          : 231,
            "material_consumptions_set" : [
                {
                    'material' : 3,
                    'consumption' : 0.3,
                }
            ]
        }
        

        


    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
    

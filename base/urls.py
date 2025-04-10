from django.urls import path
from base import views

# from .authentication import login
urlpatterns = [
    #Authentication
    path('token/obtain/', views.Obtain_Token, name='token_obtain_pair'),
    path('token/refresh/', views.Refresh_Token, name='token_refresh'),
    path('token/blacklist/', views.Logout_Token, name='token_blacklist'),
    

    #User
    path('user/create/', views.Create_User, name = 'Create_User'),
    path('user/<str:pk>/update/', views.Update_User, name = 'Update_User'),
    path('user/all/', views.List_User, name = 'List_User'),
    path('user/<str:pk>/', views.Get_User, name = 'Get_User'),
    


    #Branch
    path('branch/create/', views.Create_Branch, name = 'Create_Branch'),
    path('branch/<str:pk>/update/', views.Update_Branch, name = 'Update_Branch'),
    path('branch/all/', views.List_Branch, name = 'List_Branch'),
    path('branch/<str:pk>/', views.Get_Branch, name = 'Get_Branch'),
    

    #Child
    path('child/create/', views.Create_Child, name = 'Create_Child'),
    path('child/<str:pk>/update/', views.Update_Child, name = 'Update_Child'),
    path('child/all/', views.List_Child, name = 'List_Child'),
    path('child/non_active/all/', views.List_NonActiveChild, name = 'List_NonActiveChild'),
    path('child/<str:pk>/', views.Get_Child, name = 'Get_Child'),
    
    #School
    path('school/create/', views.Create_School, name = 'Create_School'),
    path('school/<str:pk>/update/', views.Update_School, name = 'Update_School'),
    path('school/all/', views.List_School, name = 'List_School'),
    path('school/<str:pk>/', views.Get_School, name = 'Get_School'),

    #Staff
    path('staff/create/', views.Create_Staff, name = 'Create_Staff'),
    path('staff/<str:pk>/update/', views.Update_Staff, name = 'Update_Staff'),
    path('staff/all/', views.List_Staff, name = 'List_Staff'),
    path('staff/<str:pk>/', views.Get_Staff, name = 'Get_Staff'),

    #StaffWithdraw
    path('staff_withdraw/create/', views.Create_StaffWithdraw, name = 'Create_StaffWithdraw'),
    path('staff_withdraw/<str:pk>/update/', views.Update_StaffWithdraw, name = 'Update_StaffWithdraw'),
    path('staff_withdraw/all/', views.List_StaffWithdraw, name = 'List_StaffWithdraw'),
    path('staff_withdraw/<str:pk>/', views.Get_StaffWithdraw, name = 'Get_StaffWithdraw'),

    #StaffFine
    path('staff_fine/create/', views.Create_StaffFine, name = 'Create_StaffFine'),
    path('staff_fine/<str:pk>/update/', views.Update_StaffFine, name = 'Update_StaffFine'),
    path('staff_fine/all/', views.List_StaffFine, name = 'List_StaffFine'),
    path('staff_fine/<str:pk>/', views.Get_StaffFine, name = 'Get_StaffFine'),

    #StaffSalary
    path('staff_salary/create/', views.Create_StaffSalary, name = 'Create_StaffSalary'),
    path('staff_salary/<str:pk>/update/', views.Update_StaffSalary, name = 'Update_StaffSalary'),
    path('staff_salary/all/', views.List_StaffSalary, name = 'List_StaffSalary'),
    path('staff_salary/<str:pk>/', views.Get_StaffSalary, name = 'Get_StaffSalary'),

    #Product
    path('product/create/', views.Create_Product, name = 'Create_Product'),
    path('product/<str:pk>/update/', views.Update_Product, name = 'Update_Product'),
    path('product/all/', views.List_Product, name = 'List_Product'),
    path('product/<str:pk>/', views.Get_Product, name = 'Get_Product'),

    #BranchProduct
    path('branch_product/create/', views.Create_BranchProduct, name = 'Create_BranchProduct'),
    path('branch_product/<str:pk>/update/', views.Update_BranchProduct, name = 'Update_BranchProduct'),
    path('branch_product/all/', views.List_BranchProduct, name = 'List_BranchProduct'),
    path('branch_product/<str:pk>/', views.Get_BranchProduct, name = 'Get_BranchProduct'),

    #Material
    path('material/create/', views.Create_Material, name = 'Create_Material'),
    path('material/<str:pk>/update/', views.Update_Material, name = 'Update_Material'),
    path('material/all/', views.List_Material, name = 'List_Material'),
    path('material/<str:pk>/', views.Get_Material, name = 'Get_Material'),

    #BranchMaterial
    path('branch_material/create/', views.Create_BranchMaterial, name = 'Create_BranchMaterial'),
    path('branch_material/<str:pk>/update/', views.Update_BranchMaterial, name = 'Update_BranchMaterial'),
    path('branch_material/all/', views.List_BranchMaterial, name = 'List_BranchMaterial'),
    path('branch_material/<str:pk>/', views.Get_BranchMaterial, name = 'Get_BranchMaterial'),

    #Bill
    path('bill/create/', views.Create_Bill, name = 'Create_Bill'),
    path('bill/<str:pk>/close/', views.Close_Bill, name = 'Close_Bill'),
    path('bill/<str:pk>/apply_discount/', views.Apply_Discount_Bill, name = 'Apply_Discount_Bill'),
    path('bill/all/', views.List_Bill, name = 'List_Bill'),
    path('bill/active/all/', views.List_ActiveBill, name = 'List_ActiveBill'),
    path('bill/<str:pk>/', views.Get_Bill, name = 'Get_Bill'),

    #ProductBill
    path('product_bill/create/', views.Create_ProductBill, name = 'Create_ProductBill'),
    path('product_bill/<str:pk>/update/', views.Update_ProductBill, name = 'Update_ProductBill'),
    path('product_bill/all/', views.List_ProductBill, name = 'List_ProductBill'),
    path('product_bill/active/all/', views.List_ActiveProductBill, name = 'List_ActiveProductBill'),
    path('product_bill/<str:pk>/', views.Get_ProductBill, name = 'Get_ProductBill'),

    #Discount
    path('discount/create/', views.Create_Discount, name = 'Create_Discount'),
    path('discount/<str:pk>/update/', views.Update_Discount, name = 'Update_Discount'),
    path('discount/all/', views.List_Discount, name = 'List_Discount'),
    path('discount/<str:pk>/', views.Get_Discount, name = 'Get_Discount'),

    #GeneralExpense
    path('general_expense/create/', views.Create_GeneralExpense, name = 'Create_GeneralExpense'),
    path('general_expense/<str:pk>/update/', views.Update_GeneralExpense, name = 'Update_GeneralExpense'),
    path('general_expense/all/', views.List_GeneralExpense, name = 'List_GeneralExpense'),
    path('general_expense/<str:pk>/', views.Get_GeneralExpense, name = 'Get_GeneralExpense'),

    #MaterialExpense
    path('material_expense/create/', views.Create_MaterialExpense, name = 'Create_MaterialExpense'),
    path('material_expense/<str:pk>/update/', views.Update_MaterialExpense, name = 'Update_MaterialExpense'),
    path('material_expense/all/', views.List_MaterialExpense, name = 'List_MaterialExpense'),
    path('material_expense/<str:pk>/', views.Get_MaterialExpense, name = 'Get_MaterialExpense'),

    #Subscription
    path('subscription/create/', views.Create_Subscription, name = 'Create_Subscription'),
    path('subscription/<str:pk>/update/', views.Update_Subscription, name = 'Update_Subscription'),
    path('subscription/all/', views.List_Subscription, name = 'List_Subscription'),
    path('subscription/<str:pk>/', views.Get_Subscription, name = 'Get_Subscription'),

    #SubscriptionInstance
    path('subscription_instance/create/', views.Create_SubscriptionInstance, name = 'Create_SubscriptionInstance'),
    path('subscription_instance/<str:pk>/update/', views.Update_SubscriptionInstance, name = 'Update_SubscriptionInstance'),
    path('subscription_instance/all/', views.List_SubscriptionInstance, name = 'List_SubscriptionInstance'),
    path('subscription_instance/<str:pk>/', views.Get_SubscriptionInstance, name = 'Get_SubscriptionInstance'),

    #Offer
    path('offer/create/', views.Create_Offer, name = 'Create_Offer'),
    path('offer/<str:pk>/update/', views.Update_Offer, name = 'Update_Offer'),
    path('offer/all/', views.List_Offer, name = 'List_Offer'),
    path('offer/<str:pk>/', views.Get_Offer, name = 'Get_Offer'),

    #BranchOffer
    path('branch_offer/create/', views.Create_BranchOffer, name = 'Create_BranchOffer'),
    path('branch_offer/<str:pk>/update/', views.Update_BranchOffer, name = 'Update_BranchOffer'),
    path('branch_offer/all/', views.List_BranchOffer, name = 'List_BranchOffer'),
    path('branch_offer/<str:pk>/', views.Get_BranchOffer, name = 'Get_BranchOffer'),

    #Cashier
    path('cashier/create/', views.Create_Cashier, name = 'Create_Cashier'),
    path('cashier/all/', views.List_Cashier, name = 'List_Cashier'),
]
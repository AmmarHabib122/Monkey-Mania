from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None, **extra_fields):
        if not (phone_number or username):
            raise ValueError("This field must be set")
        
        # email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, username = username, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault("is_active", True)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, username, password, **extra_fields)
    

    


class User(AbstractBaseUser, PermissionsMixin):

    username     = models.CharField(max_length = 150, unique = True)
    phone_number = models.CharField(max_length = 20, unique = True)
    email        = models.EmailField(null = True, blank = True, unique = True)
    role         = models.CharField(max_length = 10, null = True)
    created      = models.DateTimeField(auto_now_add = True)
    updated      = models.DateTimeField(auto_now = True)
    last_logout  = models.DateTimeField(null = True, blank = True)
    created_by   = models.ForeignKey('self', on_delete = models.PROTECT, null = True, related_name = 'created_users_set')
    is_active    = models.BooleanField(default=True)
    branch       = models.ForeignKey('base.Branch', on_delete = models.PROTECT, null = True, blank = True, related_name = 'users_set')
    staff        = models.ForeignKey('base.staff', on_delete = models.SET_NULL, null = True, blank = True, related_name = 'get_user')    
    is_superuser = models.BooleanField(default=False)  #used for admin panel
    is_staff     = models.BooleanField(default=False)  #used for admin panel
   #last_login already exists
   #staff.id


    objects = CustomUserManager()

    USERNAME_FIELD  = 'phone_number'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"#{self.id} {self.username}"
    
    







































































    # class UserCustomManager(BaseUserManager):
#     def _create_user(self, phone_number, password, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not phone_number:
#             raise ValueError("The given phone number must be set")
#         # Lookup the real model class from the global app registry so this
#         # manager method can be used in migrations. This is fine because
#         # managers are by definition working on the real model.
#         try:
#             validate_password(password)
#         except ValidationError as e:
#             raise ValidationError({'password': e.messages})
        
#         user = self.model(phone_number=phone_number,  **extra_fields)
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user
    



#     def create_superuser(self, phone_number, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(phone_number, password, **extra_fields)
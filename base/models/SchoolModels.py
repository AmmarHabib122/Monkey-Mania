from django.db import models



class School(models.Model):
    name                 = models.CharField(max_length = 150, unique = True)
    address              = models.CharField(max_length = 255)
    notes                = models.CharField(max_length = 255, null = True, blank = True)
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_schools_set')
    
    
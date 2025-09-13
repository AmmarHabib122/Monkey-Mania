import uuid
import hashlib
from datetime import datetime
from django.db import models


def upload_to_path(instance, filename):
    folder_name = "base"
    ext = filename.split('.')[-1]          # Get file extension
    unique_name = f'{uuid.uuid4()}.{ext}'  # Generate a unique filename
    date_path = datetime.now().strftime('%Y/%m/%d')  # Format the current date
    return f'{folder_name}_photos/{date_path}/{unique_name}'





class Image(models.Model):
    value   = models.ImageField(upload_to=upload_to_path, unique=True)
    hash    = models.CharField(max_length=64, null=True, editable=False)   
    created         = models.DateTimeField(auto_now_add = True)
    updated         = models.DateTimeField(auto_now = True) 




    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.calculate_hash()
        super().save(*args, **kwargs)  # Ensure super().save() is called
    

    def calculate_hash(self):
        hasher = hashlib.sha256()
        self.value.file.seek(0)
        for chunk in self.value.chunks():
            hasher.update(chunk)
        self.value.file.seek(0)
        return hasher.hexdigest()
    
    def __str__(self):
        return f"Image {self.id} - {self.hash}"
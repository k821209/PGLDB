from django.db import models

# Create your models here.
class AI1(models.Model):
   class Meta:
      db_table = 'ai1' 
   source     = models.CharField(max_length=20)  
   target     = models.CharField(max_length=20)
   counts     = models.CharField(max_length=20)

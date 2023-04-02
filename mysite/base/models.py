from django.db import models

# Create your models here.

class prediction_chart(models.Model):
   positive = models.IntegerField()
   negative = models.IntegerField()




class contact_us_tbl(models.Model):
   name =  models.CharField(max_length=200)
   email =  models.CharField(max_length=200)
   subject =  models.CharField(max_length=200)
   phone =  models.CharField(max_length=200)
   message =  models.CharField(max_length=200)


   def __str__(self):
      return self.name
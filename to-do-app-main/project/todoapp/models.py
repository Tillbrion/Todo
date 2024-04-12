from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    tittle = models.CharField(max_length=200)
    discription = models.TextField(null=True,blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due_date= models.DateField(null=True)
    due_time = models.TimeField(null=True)


    def __str__(self):
         return self.tittle

    class Meta:
        ordering=['complete']



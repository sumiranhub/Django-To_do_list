from django.db import models
from django.contrib.auth.models import User #build in usermodel ho jasle sepcific user ko task lai link garcha
# Create your models here.

class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) #foreign key le onetomany realation dincha with user, cascade part le chai if user delete garyo vani sabai task ni delete huncha
    title=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    complete=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True) #auto now add le chai automatically current time set garcha

    def __str__(self):
        return self.title # yeni haru le chai task ko string representation lai define garcha,
    
    class Meta: #sort garna lai nested class
        ordering = ['complete'] #task lai query garda incomplete task aagai aauncha
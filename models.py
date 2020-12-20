from django.db import models

# Create your models here.
class dress_recomm(models.Model):
    dress_name=models.CharField(max_length=256)
    cos_sim=models.FloatField(null=False)

    def __str__(self):
        return self.dress_name
from django.db import models


# Create your models here.

class MyUser(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthday = models.DateField()
    photo = models.ImageField("photo", upload_to="users/photos", default="" , blank=True)
    counter = models.IntegerField(choices=[(i, i) for i in range(0, 11)], blank=True)

    def save(self, *args, **kwargs):
        for field_name in ['name', 'surname']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())


        super(MyUser, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.name} {self.surname}'



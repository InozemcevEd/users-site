from django import forms
from .models import MyUser

class CreateNewUser(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    surname = forms.CharField(label="Surname", max_length=200)
    # age = forms.IntegerField(label="Age")
    birthday = forms.DateField(label="Birthday")
    photo = forms.ImageField()
    # photo = forms.ImageField("photo", upload_to="users/photos", default="" , blank=True)
    # photo = forms.ImageField()
    

class UsersFilterForm(forms.Form):
    ordering = forms.ChoiceField(label="sort", required=False,  choices=[
        ["name", "sort name from A-Z"],
        ["-name", "sort name from Z-A"],
        ["surname", "sort surname from A-Z"],
        ["-surname", "sort surname from Z-A"],
        ["birthday", "age from oldest"],
        ["-birthday", "age from youngest"]
    ])


# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = Photo

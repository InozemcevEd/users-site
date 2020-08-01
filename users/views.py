from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MyUser
from django.template import loader
from .forms import CreateNewUser, UsersFilterForm
import xlwt
from django.utils import timezone
from datetime import datetime
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from .models import MyUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import requests

def home(response):
    all_users = MyUser.objects.all()

    print(all_users)
    form = UsersFilterForm(response.GET)
    if form.is_valid():
        if form.cleaned_data["ordering"]: 
            all_users = MyUser.objects.order_by(form.cleaned_data["ordering"])

    return render(response, 'users/home.html', {"all_users": all_users, "form": form})


def detail_information(response, user_id):
    user = MyUser.objects.get(id=user_id)

    today = timezone.now().date()

    if response.method == "POST":
        user.delete()
        return HttpResponseRedirect("/")

    age = today.year - user.birthday.year - 1
    if today.month - user.birthday.month >= 0:
        age += 1
    


    return render(response, 'users/detail.html', {"user": user, "age": age})



def create(response):
    today = timezone.now().date()
    
    if response.method == "POST":
        form = CreateNewUser(response.POST, response.FILES)

        if form.is_valid():
            data = form.cleaned_data
            new_user = MyUser(**data)
            new_user.save()

            return HttpResponseRedirect("/")
        

    else:
        form = CreateNewUser()
    return render(response, "users/create.html", {"form":form})


def save_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls" '

    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet = work_book.add_sheet('Users')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'surname', 'age', 'birthday']

    for col_num in range(len(columns)):
        work_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = MyUser.objects.all().values_list('name', 'surname', 'age', 'birthday',)

    today = timezone.now().date()
    for row in rows:
        row_num += 1
        for col_num in range(len(row) - 2):
            work_sheet.write(row_num, col_num, row[col_num], font_style)


        col_num += 1
        age = today.year - row[col_num + 1].year - 1
        if today.month - row[col_num + 1].month >= 0:
            age += 1
        work_sheet.write(row_num, col_num, age, font_style)


        col_num += 1
        date = datetime.strftime(row[col_num], '%Y-%m-%d')
        work_sheet.write(row_num, col_num, date, font_style)
    
    work_book.save(response)
    return response


def votes(response):
    all_users = MyUser.objects.all()
    return render(response, 'users/votes.html', {"all_users": all_users})


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(['PUT'])
def api_vote(request, user_id):
    user = MyUser.objects.get(id=user_id)
    serializer = UserSerializer(user)
    if user.counter < 10:
        user.counter += 1
    user.save()
    return Response(serializer.data)

def vote(request, user_id):
    user = MyUser.objects.get(id=user_id)
    requests.put(f'http://127.0.0.1:8000/api/myuser/{user.id}/vote/', data={})
    return HttpResponseRedirect("/votes")
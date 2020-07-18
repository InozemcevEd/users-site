from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MyUser
from django.template import loader
from .forms import CreateNewUser, UsersFilterForm
import xlwt


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

    if response.method == "POST":
        user.delete()
        return HttpResponseRedirect("/")

    return render(response, 'users/detail.html', {"user": user})



def create(response):
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

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            work_sheet.write(row_num, col_num, row[col_num], font_style)
    
    work_book.save(response)
    return response
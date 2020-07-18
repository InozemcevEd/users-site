from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("<int:user_id>/", views.detail_information, name="detail_information"),
    path('create/', views.create, name="create"),
    path('save_users_xls/', views.save_users_xls, name="save_users_xls"),
]
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('myuser', views.UserViewSet)


urlpatterns = [
    path('', views.home, name='home'),
    path("<int:user_id>/", views.detail_information, name="detail_information"),
    path('create/', views.create, name="create"),
    path('save_users_xls/', views.save_users_xls, name="save_users_xls"),
    path('votes/', views.votes, name="votes"),
    path('api/', include(router.urls)),
    path('api/myuser/<int:user_id>/vote/', views.api_vote),
    path('vote/<int:user_id>/', views.vote),
]



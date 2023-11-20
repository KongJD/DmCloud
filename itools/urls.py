from django.urls import path
from itools import views

urlpatterns = [
    path("16s/", views.Tools16SView.as_view(), ),

]

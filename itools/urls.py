from django.urls import path
from itools import views

urlpatterns = [
    path("16s/", views.Tools16SView.as_view(), ),
    path("rpob/", views.ToolsRpobView.as_view(), ),
    path("bactiergenome/", views.ToolsGeneProcessView.as_view(), ),
    path("report/", views.Tools16sRpobResultView.as_view(), ),
    path('t/', views.TaskTest.as_view(), ),

]

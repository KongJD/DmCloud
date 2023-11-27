from django.urls import path
from itools import views

urlpatterns = [
    path("16s/", views.Tools16SView.as_view(), ),
    path("rpob/", views.ToolsRpobView.as_view(), ),
    path("its/", views.ItoolsItsView.as_view(), ),
    path("bactiergenome/", views.ToolsGeneProcessView.as_view(), ),
    path("report/", views.Tools16sRpobResultView.as_view(), ),
    path("bacteria_report/", views.GenerprocessResultView.as_view(), ),
    path("unread/", views.UserGetUserNotificationView.as_view(), ),
    path("unreadchange/", views.UnreadChangeView.as_view(), ),
    path("upload/", views.UploadView.as_view()),
    # path('t/', views.TaskTest.as_view(), ),
    path('p/', views.notice, ),

]

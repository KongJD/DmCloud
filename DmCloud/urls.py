"""DmCloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import notifications.urls
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from DmCloud import settings
from itools.views import MyTokenObtainPairView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('baike/', include('baike.urls')),
                  path('itools/', include('itools.urls')),
                  url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
                  path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

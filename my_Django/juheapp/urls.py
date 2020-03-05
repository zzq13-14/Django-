"""my_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from apps import views
from juheapp import views

urlpatterns = [
    # path('index/',views.index),
    # path('admin/', admin.site.urls),
    #     # path('apps/',include('apps.urls')),
    #     # path('api/v1.0/',include('apps.urls'))
    path('juhe/',views.index),
    path('juhes/',views.testindex),
    path('image/',views.image),
    path('image1/',views.ImageView.as_view()),
    path('imagetext/',views.ImageText.as_view()),
    path('cookietest/',views.CookieTest.as_view()),
    path('cookietest2/',views.CookieTest2.as_view()),
    path('authorize/',views.Authorize.as_view()),
    path('user/',views.UserView.as_view()),
    path('logout/',views.Logout.as_view()),
    path('status/',views.Status.as_view()),
    path('citys/',views.weather),
    path('weather/',views.Weather.as_view()),




    path('apps/',views.apps)
]

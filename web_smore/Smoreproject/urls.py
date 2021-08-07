"""Smoreproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from account import views as A
from smore import views as S

urlpatterns = [
    path('admin/', admin.site.urls),
    path('smore/home', S.home, name='home'),
    path('account/signup', A.signup, name="signup"),
    path('account/user_login/', A.user_login, name="user_login"),
    path('account/user_logout/',A.user_logout, name="user_logout"),
    path('account/mypage_edit/<str:id>',A.mypage_edit, name="mypage_edit"),
    path('account/mypage/<str:id>',A.mypage, name="mypage"),
    path('smore/create', S.create, name="create"),
    path('smore/detail/<str:id>', S.detail, name="detail"),
    path('smore/edit/<str:id>', S.edit, name="edit"),
    path('smore/delete/<str:id>', S.delete, name='delete'),
    path('smore/experience/', S.experience, name="experience"),
    path('smore/exper_create', S.exper_create, name="exper_create"),
    path('smore/exper_detail/<str:id>', S.exper_detail, name="exper_detail"),
    path('smore/exper_edit/<str:id>', S.exper_edit, name="exper_edit"),
    path('smore/exper_delete/<str:id>', S.exper_delete, name="exper_delete"),
    path('', S.main_chart, name="main_chart"),
    path('com_chart',S.com_chart, name="com_chart"),
    path('product_chart', S.product_chart, name="product_chart"),
    path('research_chart', S.research_chart, name="research_chart"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

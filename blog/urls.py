"""tut1 URL Configuration

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
from blog import views

urlpatterns = [
   
    path('', views.home, name='home'),
    path('addpost', views.addpost, name="addpost"),

    path('post/<int:pk>', views.single_post, name="single_post"),
    path('search', views.search, name="search_text"),
    # path('addprofile', views.addprofile, name="addprofile"),
    path('signup', views.signup, name="signup"),
    path('login', views.login_, name="login"),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('edit_post/<int:pk>', views.edit_post, name="edit_post"),
    path('edit_profile/<int:pk>', views.edit_profile, name="edit_profile"),
    path('log_out', views.log_out, name="log_out"),
    path('delete', views.delete, name="delete"),
    path('delete_post/<int:pk>', views.delete_post, name="delete_post"),
    # path('forgot_pass', views.forgot_pass, name="forgot_pass")
]

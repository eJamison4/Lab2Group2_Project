"""
URL configuration for Lab2Group2_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from TA_Scheduler_App.views import Login, Account, Dashboard, Courses, AddSection

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', Login.as_view(), name = "login"),
    path('accounts/', Account.as_view(), name = 'accounts'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('courses/', Courses.as_view(), name='courses'),
    path(
        "courses/<int:course_id>/add-section/",
        AddSection.as_view(),
        name="add-section",
    ),
]

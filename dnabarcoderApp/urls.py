"""dnabarcoderApp URL Configuration

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
import apps.Interface.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main page redirects to classification page:
    path('', views.redirect_classification),
    path('cutoff', views.cutoff_page, name='cutoff'),
    path('cutoff/settings', views.cutoff_settings_page),
    path('classification', views.classification_page, name='classification'),
    path('classification/settings', views.classification_settings_page),
    path('classification/results', views.classification_results_page),
    path('visualization', views.visualization_page, name='visualization'),
]

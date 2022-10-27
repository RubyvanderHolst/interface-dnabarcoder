"""interface-dnabarcoder URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings
import apps.Interface.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main page redirects to classification page:
    path('', views.redirect_classification),
    path('cutoff', views.cutoff_page, name='cutoff'),
    path('cutoff/results', views.cutoff_results_page, name='cutoff_results'),
    path('cutoff/<task_id>', views.load_progress, name='load_progress'),
    path('classification', views.classification_page, name='classification'),
    path('classification/results', views.classification_results_page),
    path('visualization', views.visualization_page, name='visualization'),
]

# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
import apps.Cutoff.views as cutoff_views
import apps.Classification.views as class_views
import apps.Visualization.views as vis_views
import apps.Other.views as other_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main page redirects to classification page:
    path('', class_views.redirect_classification),
    path('cutoff', cutoff_views.cutoff_page,
         name='cutoff'),
    path('cutoff/results', cutoff_views.cutoff_results_page,
         name='cutoff_results'),
    path('cutoff/<task_id>', cutoff_views.load_progress,
         name='load_progress_cutoff'),
    path('classification', class_views.classification_page,
         name='classification'),
    path('classification/results', class_views.classification_results_page,
         name='classification_results'),
    path('classification/<task_id>', class_views.load_progress,
         name='load_progress_classification'),
    path('visualization', vis_views.visualization_page,
         name='visualization'),
    path('about', other_views.about_page,
         name='about')
]

# only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

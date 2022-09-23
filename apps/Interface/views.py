from django.shortcuts import render, redirect
import numpy as np


def redirect_classification(self):
    return redirect('/classification')


def cutoff_page(request):
    return render(request, 'cutoff.html')


def cutoff_settings_page(request):
    return render(request, 'cutoff_settings.html')


def classification_page(request):
    return render(request, 'classification.html', {
        'test': request.path,
    })


def classification_settings_page(request):
    return render(request, 'classification_settings.html')


def visualization_page(request):
    return render(request, 'visualization.html')

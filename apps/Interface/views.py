from django.shortcuts import render, redirect
import numpy as np
import os


def redirect_classification(self):
    return redirect('/classification')


def cutoff_page(request):
    return render(request, 'cutoff.html')


def cutoff_settings_page(request):
    return render(request, 'cutoff_settings.html')


def classification_page(request):
    # This is going to change with server connection
    path = "/home/app/data"
    list_files = os.listdir(path)
    return render(request, 'classification.html', {
        'test': list_files,
    })


def classification_settings_page(request):
    return render(request, 'classification_settings.html')


def classification_results_page(request):
    return render(request, 'classification_results.html')


def visualization_page(request):
    return render(request, 'visualization.html')


from django.shortcuts import render, redirect
import numpy as np
import os


def redirect_classification(self):
    return redirect('/classification')


def cutoff_page(request):
    return render(request, 'cutoff.html')


# def cutoff_settings_page(request):
#     return render(request, 'cutoff_settings.html')

def cutoff_results_page(request):
    return render(request, 'cutoff_results.html')


def classification_page(request):
    path = "/home/app/data"
    list_files = os.listdir(path)
    return render(request, 'classification.html', {
        'list_files': list_files,
    })



def classification_results_page(request):

    test = request.POST
    return render(request, 'classification_results.html',{
        'test': test,
    })


def visualization_page(request):
    return render(request, 'visualization.html')


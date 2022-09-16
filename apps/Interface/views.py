from django.shortcuts import render
import numpy as np

def main_page(request):
    a = 'hallo'
    return render(request, 'main.html', {'test': a})


def cutoff_page(request):
    return render(request, 'cutoff.html')


def classification_page(request):
    return render(request, 'classification.html')


def visualization_page(request):
    return render(request, 'visualization.html')

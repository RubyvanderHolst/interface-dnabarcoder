from django.shortcuts import render


def main_page(request):
    return render(request, 'main.html')


def cutoff_page(request):
    return render(request, 'cutoff.html')


def classification_page(request):
    return render(request, 'classification.html')


def visualization_page(request):
    return render(request, 'visualization.html')

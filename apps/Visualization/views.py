from django.shortcuts import render


def visualization_page(request):
    return render(request, 'visualization.html')

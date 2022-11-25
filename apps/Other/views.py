from django.shortcuts import render

def about_page(request):
    # View for about page
    return render(request, 'about.html')

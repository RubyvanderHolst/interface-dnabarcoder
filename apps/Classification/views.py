from django.shortcuts import render, redirect
from .forms import ClassificationForm


def redirect_classification(self):
    return redirect('/classification')


def classification_page(request):
    form = ClassificationForm
    return render(request, 'classification.html', {
        'form': form,
    })


def classification_results_page(request):
    test = request.POST
    file = open('/media/testbestand.txt', 'w')
    file.write(str(test))
    file.close()
    return render(request, 'classification_results.html', {
        'test': test,
    })

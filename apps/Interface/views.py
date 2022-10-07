from django.shortcuts import render, redirect
import numpy as np
import celery
import os


def redirect_classification(self):
    return redirect('/classification')


def cutoff_page(request):
    return render(request, 'cutoff.html')


def cutoff_results_page(request):
    test = request.POST

    dnabarcoder_path = "/home/tool/dnabarcoder.py"
    input_bestand_path = request.FILES['input_reference'].temporary_file_path()
    rank = request.POST['rank']
    higher_rank = request.POST['higher_rank']
    min_alignment_length = request.POST['min_alignment_length']

    output = os.popen(f"python {dnabarcoder_path} "
                      f"predict "
                      f"--input {input_bestand_path} "
                      # f"--startingthreshold 0.7 "
                      # f"--endthreshold 1 "
                      # f"--step 0.001 "
                      f"-rank {rank} "
                      f"-higherrank {higher_rank} "
                      f"--minalignmentlength {min_alignment_length} "
                      f"-prefix cutoff_result "
                      f"-o /home/app/static/results ").read()
    return render(request, 'cutoff_results.html', {
        'test': test,
        'output': output,
    })


def classification_page(request):
    # Get the already available reference files
    path = "/home/app/data"
    list_files = os.listdir(path)
    return render(request, 'classification.html', {
        'list_files': list_files,
    })


def classification_results_page(request):
    test = request.POST
    file = open('/home/app/static/results/testbestand.txt', 'w')
    file.write(str(test))
    file.close()
    return render(request, 'classification_results.html', {
        'test': test,
    })


def visualization_page(request):
    return render(request, 'visualization.html')

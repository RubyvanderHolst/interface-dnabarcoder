from django.shortcuts import render, redirect
import numpy as np
import celery
import os


def redirect_classification(self):
    return redirect('/classification')


def cutoff_page(request):
    return render(request, 'cutoff.html')


def cutoff_results_page(request):
    dnabarcoder_path = "/home/tool/dnabarcoder.py"

    input_file_path = request.FILES['input_reference'].temporary_file_path()

    sim_file_path = None
    if 'sim_file' in request.FILES:
        sim_file_path = request.FILES['sim_file'].temporary_file_path()

    min_alignment_length = request.POST['min_alignment_length']

    rank = request.POST['rank']

    higher_rank = None
    if 'higher_rank' in request.POST:
        higher_rank = request.POST['higher_rank']

    starting_threshold = request.POST['starting_threshold']
    end_threshold = request.POST['end_threshold']
    step = request.POST['step']

    min_group_number = request.POST['min_group_number']
    min_seq_number = request.POST['min_seq_number']

    command = f"python {dnabarcoder_path} "\
              f"predict "\
              f"--input {input_file_path} "\
              f"--simfilename {sim_file_path} "\
              f"--minalignmentlength {min_alignment_length} "\
              f"-rank {rank} "\
              f"-higherrank {higher_rank} "\
              f"--startingthreshold {starting_threshold} "\
              f"--endthreshold {end_threshold} "\
              f"--step {step} "\
              f"-mingroupno {min_group_number} "\
              f"-minseqno {min_seq_number} "\
              f"-prefix cutoff_result "\
              f"-o /home/app/static/results "

    output = os.popen(command).read()
    return render(request, 'cutoff_results.html', {
        'test': command,
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

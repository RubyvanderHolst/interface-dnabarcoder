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
    max_seq_number = request.POST['max_seq_number']


    # Remove sequences of the same complex
    output2 = "..."
    rem_comp_1 = "no"
    if 'remove_comp' in request.POST:
        end_threshold = request.POST['cutoff_remove']
        if end_threshold == "1":
            rem_comp_1 = "yes"
        else:
            remove_command = f"python {dnabarcoder_path} "\
                             f"remove "\
                             f"--input {input_file_path} "\
                             f"--cutoff {end_threshold} "\
                             f"--minalignmentlength {min_alignment_length} "\
                             f"--classificationrank {rank} "\
                             f"--out /home/app/static/results "
            if sim_file_path != None:
                remove_command += f"--simfilename {sim_file_path} "
            output2 = os.popen(remove_command).read()
            input_file_path = "/home/app/static/results/" +\
                               input_file_path.split('/')[-1].\
                                   replace('fasta', 'diff.fasta')

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
              f"-minseqno {min_seq_number} " \
              f"-maxseqno {max_seq_number} " \
              f"-removecomplexes {rem_comp_1} "\
              f"-prefix cutoff_result "\
              f"--out /home/app/static/results "


    output = os.popen(command).read()
    return render(request, 'cutoff_results.html', {
        'test': output2,
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

from django.shortcuts import render, redirect
from .forms import CutoffForm, ClassificationForm
from django.core.files.storage import FileSystemStorage
import numpy as np
import celery
import os


def redirect_classification(self):
    return redirect('/classification')


def cutoff_page(request):
    form = CutoffForm
    return render(request, 'cutoff.html', {
        'form': form,
    })


def cutoff_results_page(request):
    input_dir = "media/uploaded"
    fs = FileSystemStorage(input_dir)
    output_dir = "media/cutoff"
    os.system(f"rm {input_dir}/* &&"
              f"rm {output_dir}/*")


    dnabarcoder_path = "/home/tool/dnabarcoder.py"
    input_file = request.FILES['input_file']
    file = fs.save(input_file.name, input_file)
    input_file_path = os.path.join(input_dir, input_file.name)

    sim_file_path = None
    if 'sim_file' in request.FILES:
        sim_file = request.FILES['sim_file']
        file = fs.save(sim_file.name, sim_file)
        sim_file_path = os.path.join(input_dir, sim_file.name)

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
                             f"--out {output_dir} "
            if sim_file_path != None:
                remove_command += f"--simfilename {sim_file_path} "
            input_file_path = output_dir +\
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
              f"--out {output_dir} "

    output = os.popen(command).read()
    os.system(f"cd {output_dir} && "
              "rm tmp*")
    os.system("cd /home/app/ && "
              "rm db.n*")


    dict_files = get_file_sizes(output_dir)  # {file_name: [file_path, file_size]}
    image_files = []
    for file_name in dict_files.keys():
        if file_name[-4:] == '.png':
            image_files.append(file_name)

    return render(request, 'cutoff_results.html', {
        'output': output,
        'files': dict_files,
        'images': image_files,
    })


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

def get_file_sizes(dir_path):
    # Get the sizes of all files in a directory
    # Return dictionary: {file_name: [file_path, file_size]}
    paths_list = [os.path.join(dir_path, file) for file in os.listdir(dir_path)]
    dict_files = {}
    for path in paths_list:
        name = os.path.basename(path)
        size = os.stat(path).st_size
        dict_files[name] = [path, size]
    return dict_files


def visualization_page(request):
    return render(request, 'visualization.html')


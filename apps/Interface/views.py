from django.shortcuts import render, redirect
from .forms import CutoffForm, ClassificationForm
from django.core.files.storage import FileSystemStorage
import numpy as np
import os


def redirect_classification(self):
    return redirect('/classification')


def cutoff_page(request):
    form = CutoffForm
    return render(request, 'cutoff.html', {
        'form': form,
    })


def cutoff_results_page(request):
    # Retrieve data from request
    input_dir = "media/uploaded"
    fs = FileSystemStorage(input_dir)
    output_dir = "media/cutoff"
    os.system(f"rm {input_dir}/* &&"
              f"rm {output_dir}/*")


    dnabarcoder_path = "/home/tool/dnabarcoder.py"
    input_file = request.FILES['input_file']
    file = fs.save(input_file.name, input_file)
    input_file_path = os.path.join(input_dir, input_file.name)
    prefix = input_file.name.split('.')[0]

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

    calculate_cutoff(dnabarcoder_path, input_file_path, sim_file_path,
                     min_alignment_length, rank, higher_rank, starting_threshold,
                     end_threshold, step, min_group_number, min_seq_number,
                     max_seq_number, rem_comp_1, prefix, output_dir)

    dict_files, dict_images = get_file_sizes(output_dir)

    return render(request, 'cutoff_results.html', {
        # 'output': output,
        'files': dict_files,
        'images': dict_images,
        'media_dir': 'cutoff',
    })


def calculate_cutoff(dnabarcoder_path, input_file_path, sim_file_path,
                     min_alignment_length, rank, higher_rank, starting_threshold,
                     end_threshold, step, min_group_number, min_seq_number,
                     max_seq_number, rem_comp_1, prefix, output_dir):
    command = f"python {dnabarcoder_path} " \
              f"predict " \
              f"--input {input_file_path} " \
              f"--simfilename {sim_file_path} " \
              f"--minalignmentlength {min_alignment_length} " \
              f"-rank {rank} " \
              f"-higherrank {higher_rank} " \
              f"--startingthreshold {starting_threshold} " \
              f"--endthreshold {end_threshold} " \
              f"--step {step} " \
              f"-mingroupno {min_group_number} " \
              f"-minseqno {min_seq_number} " \
              f"-maxseqno {max_seq_number} " \
              f"-removecomplexes {rem_comp_1} " \
              f"-prefix {prefix} " \
              f"--out {output_dir} "

    os.system(command)

    os.system(f"cd {output_dir} && "
              "rm tmp*")
    os.system("cd /home/app/ && "
              "rm db.n*")


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
    # Return two dictionaries: {file_name: file_size}
    # one for images and one for all other files
    file_list = os.listdir(dir_path)
    dict_files = {}
    dict_images = {}
    for name in file_list:
        size = bytes_to_larger(os.stat(os.path.join(dir_path, name)).st_size)
        if name[-4:] == '.png':
            dict_images[name] = size
        else:
            dict_files[name] = size
    return dict_files, dict_images


def bytes_to_larger(size_b):
    sizes = ['TB', 'GB', 'MB', 'KB', 'B']
    x = 10**((len(sizes) - 1) * 3)
    for size in sizes:
        if size_b > x:
            return f"{int(size_b / x)} {size}"
        else:
            x *= 10**-3

def visualization_page(request):
    return render(request, 'visualization.html')


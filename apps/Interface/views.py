from django.shortcuts import render, redirect
from .forms import CutoffForm, ClassificationForm
from .tasks import calculate_cutoff as cal_cut
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
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
    if request.method == 'POST':
        # Retrieve data from request
        input_dir = "media/uploaded"
        fs = FileSystemStorage(input_dir)
        output_dir = "media/cutoff"
        os.system(f"rm /home/app/{input_dir}/* &&"
                  f"rm /home/app/{output_dir}/*")


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
        #
        task = cal_cut.delay(dnabarcoder_path, input_file_path,
                                           sim_file_path, min_alignment_length,
                                           rank, higher_rank, starting_threshold,
                                           end_threshold, step, min_group_number,
                                           min_seq_number, max_seq_number,
                                           rem_comp_1, prefix, output_dir)

        task_id = task.id

    # result = AsyncResult(task_id)
    return render(request, 'cutoff_results.html', {
        # 'output': result,
        'media_dir': 'cutoff',
        'task_id': task_id,
        })

def load_progress(request, task_id):
    result = AsyncResult(task_id)
    if result.state == 'SUCCESS':
        files  =  result.info[0]
        images = result.info[1]
    else:
        files = None
        images = None
    return JsonResponse({
        'task_id': task_id,
        'state': result.state,
        'files': files,
        'images': images,
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


def visualization_page(request):
    return render(request, 'visualization.html')


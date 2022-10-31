from django.shortcuts import render, redirect
from .forms import CutoffForm
from .tasks import calculate_cutoff
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os


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

        if 'remove_comp' in request.POST:
            threshold = request.POST['cutoff_remove']
        else:
            threshold = None

        task = calculate_cutoff.delay(dnabarcoder_path, input_file_path,
                             sim_file_path, min_alignment_length, rank,
                             higher_rank, starting_threshold, end_threshold,
                             step, min_group_number, min_seq_number,
                             max_seq_number, threshold, prefix, output_dir)

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

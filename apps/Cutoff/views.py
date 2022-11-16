from .forms import CutoffForm
from .tasks import calculate_cutoff

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings

from celery.result import AsyncResult
import os


media_root = settings.MEDIA_ROOT


def cutoff_page(request):
    form = CutoffForm
    return render(request, 'cutoff.html', {
        'form': form,
    })


def cutoff_results_page(request):
    if request.method == 'POST':
        # Retrieve data from request
        input_dir = os.path.join(media_root, "uploaded")
        fs = FileSystemStorage(input_dir)
        output_dir = os.path.join(media_root, "cutoff")
        os.system(f"rm {input_dir}/* &&"
                  f"rm {output_dir}/*")

        input_file = request.FILES['input_file']
        fs.save(input_file.name, input_file)
        input_file_path = os.path.join(input_dir, input_file.name)
        prefix = input_file.name.split('.')[0]

        sim_file_path = None
        if 'sim_file' in request.FILES:
            sim_file = request.FILES['sim_file']
            fs.save(sim_file.name, sim_file)
            sim_file_path = os.path.join(input_dir, sim_file.name)
        min_alignment_length = request.POST['min_alignment_length']
        rank = request.POST['rank']
        higher_rank = retrieve_input('higher_rank', request.POST)
        starting_threshold = request.POST['starting_threshold']
        end_threshold = request.POST['end_threshold']
        step = request.POST['step']
        min_group_number = request.POST['min_group_number']
        min_seq_number = request.POST['min_seq_number']
        max_seq_number = request.POST['max_seq_number']

        threshold = None
        if 'remove_comp' in request.POST:
            threshold = request.POST['cutoff_remove']

        task = calculate_cutoff.delay(input_file_path,
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


def retrieve_input(post_key, request_POST):
    if post_key in request_POST:
        return request_POST[post_key]
    else:
        return None


def load_progress(request, task_id):
    result = AsyncResult(task_id)
    files = None
    images = None
    similar = None
    if result.state == 'SUCCESS':
        files  =  result.info[0]
        images = result.info[1]
        similar = result.info[2]
    return JsonResponse({
        'task_id': task_id,
        'state': result.state,
        'files': files,
        'images': images,
        'similar': similar,
    })

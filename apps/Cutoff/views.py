from .forms import CutoffForm
from .tasks import calculate_cutoff

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings

from celery.result import AsyncResult
import os


media_root = settings.MEDIA_ROOT
all_rank = ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']


def cutoff_page(request):
    # View for cutoff input page
    form = CutoffForm
    return render(request, 'cutoff.html', {
        'form': form,
    })


def cutoff_results_page(request, task_id=None):
    # View for cutoff results page

    # if is redirected from input page
    if request.method == 'POST':
        # Retrieve data from request
        input_dir = os.path.join(media_root, "uploaded")
        fs = FileSystemStorage(input_dir)
        output_dir = os.path.join(media_root, "results")

        input_file = request.FILES['input_file']
        input_file_fs = fs.save(input_file.name, input_file)
        input_file_path = fs.path(input_file_fs)
        prefix = input_file.name.split('.')[0]

        sim_file_path = None
        if 'sim_file' in request.FILES:
            sim_file = request.FILES['sim_file']
            sim_file_fs = fs.save(sim_file.name, sim_file)
            sim_file_path = fs.path(sim_file_fs)
        min_alignment_length = request.POST['min_alignment_length']
        rank = request.POST['rank']
        if rank == 'all':
            rank = ','.join(all_rank)
        higher_rank = retrieve_input('higher_rank', request.POST)
        if higher_rank == 'all':
            i_rank = all_rank.index(rank)
            higher_rank = ','.join(all_rank[i_rank+1:])
        starting_threshold = request.POST['starting_threshold']
        end_threshold = request.POST['end_threshold']
        step = request.POST['step']
        min_group_number = request.POST['min_group_number']
        min_seq_number = request.POST['min_seq_number']
        max_seq_number = request.POST['max_seq_number']
        email = request.POST['email']

        remove_comp = 'no'
        if 'remove_comp' in request.POST:
            remove_comp = 'yes'

        # Start celery task
        task = calculate_cutoff.delay(input_file_path,
                             sim_file_path, min_alignment_length, rank,
                             higher_rank, starting_threshold, end_threshold,
                             step, min_group_number, min_seq_number,
                             max_seq_number, remove_comp, prefix, output_dir,
                             email)

        task_id = task.id

    # if is redirected from link (email)
    else:
        if not request.user.is_authenticated:
            return redirect('login')

    return render(request, 'cutoff_results.html', {
            'task_id': task_id,
    })


def retrieve_input(post_key, request_POST):
    # Checks if input exist and returns this
    # If it does not exist, None is returned
    if post_key in request_POST:
        return request_POST[post_key]
    else:
        return None


def load_progress(request, task_id):
    # Checks state of celery task and returns results if task is done
    result = AsyncResult(task_id)
    files = None
    images = None
    # similar = None
    has_results = None
    if result.state == 'SUCCESS':
        files  =  result.info[0]
        images = result.info[1]
        # similar = result.info[2]
        has_results = result.info[2]
    return JsonResponse({
        'task_id': task_id,
        'state': result.state,
        'files': files,
        'images': images,
        # 'similar': similar,
        'has_results': has_results,
    })

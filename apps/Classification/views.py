from django.shortcuts import render, redirect
from .forms import ClassificationForm
from .tasks import classify_blast
from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os
from apps.Cutoff.views import retrieve_input


def redirect_classification(self):
    return redirect('/classification')


def classification_page(request):
    form = ClassificationForm
    return render(request, 'classification.html', {
        'form': form,
    })


def classification_results_page(request):
    if request.method == 'POST':
        # Retrieve data from request
        input_dir = "media/uploaded"
        fs = FileSystemStorage(input_dir)
        output_dir = "media/classification"
        os.system(f"rm /home/app/{input_dir}/* &&"
                  f"rm /home/app/{output_dir}/*")

        if 'file_input_sequences' in request.FILES:
            file_input_sequences = request.FILES['file_input_sequences']
            fs.save(file_input_sequences.name, file_input_sequences)
            input_sequences_path = os.path.join(input_dir,
                                                file_input_sequences.name)
        else:
            sequences = request.POST['text_input_sequences']
            input_sequences_path = os.path.join(input_dir,
                                                'input.fasta')
            file = open(input_sequences_path, 'w')
            file.write(sequences)
            file.close()

        reference_choice = request.POST['reference_options']
        if reference_choice == '':
            reference_file = request.FILES['input_reference']
            fs.save(reference_file.name, reference_file)
            reference_path = os.path.join(input_dir,
                                          reference_file.name)
        else:
            reference_path = os.path.join("reference_files", reference_choice)

        cutoff_type = request.POST['cutoff_type']
        num_cutoff = None
        file_cutoff_path = None
        if cutoff_type == 'global':
            num_cutoff = request.POST['num_cutoff']
        else:
            file_cutoff = request.FILES['file_cutoff']
            fs.save(file_cutoff.name, file_cutoff)
            file_cutoff_path = os.path.join(input_dir,
                                            file_cutoff.name)

        # min_probability = request.POST['min_probability']
        min_alignment_length = request.POST['min_alignment_length']
        confidence = retrieve_input('confidence', request.POST)
        min_group_number = retrieve_input('min_group_number', request.POST)
        min_seq_number = retrieve_input('min_seq_number', request.POST)
        rank = retrieve_input('rank', request.POST)
        # max_seq_number = request.POST['max_seq_number']

        task = classify_blast.delay(input_sequences_path, reference_path,
                                    num_cutoff, file_cutoff_path,
                                    min_alignment_length, confidence,
                                    min_group_number, min_seq_number, rank,
                                    output_dir)
        task_id = task.id

        return render(request, 'classification_results.html', {
            'media_dir': 'classification',
            'task_id': task_id,
        })


def load_progress(request, task_id):
    result = AsyncResult(task_id)
    if result.state == 'SUCCESS':
        print(result.info)
        files = result.info
    else:
        files = None
    return JsonResponse({
        'task_id': task_id,
        'state': result.state,
        'files': files,
    })
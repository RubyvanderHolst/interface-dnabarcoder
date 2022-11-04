from django.shortcuts import render, redirect
from .forms import ClassificationForm
from django.core.files.storage import FileSystemStorage
import os


def redirect_classification(self):
    return redirect('/classification')


def classification_page(request):
    form = ClassificationForm
    return render(request, 'classification.html', {
        'form': form,
    })


def classification_results_page(request):
    test = request.POST
    if request.method == 'POST':
        # Retrieve data from request
        input_dir = "media/uploaded"
        fs = FileSystemStorage(input_dir)
        output_dir = "media/classification"
        os.system(f"rm /home/app/{input_dir}/* &&"
                  f"rm /home/app/{output_dir}/*")

        dnabarcoder_path = "/home/tool/dnabarcoder.py"

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
            reference_path = os.path.join("data", reference_choice)

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

        min_probability = request.POST['min_probability']
        min_alignment_length = request.POST['min_alignment_length']
        confidence = request.POST['confidence']
        min_group_number = request.POST['min_group_number']
        min_seq_number = request.POST['min_seq_number']
        rank = request.POST['rank']
        max_seq_number = request.POST['max_seq_number']


    return render(request, 'classification_results.html', {
        'test': test,
    })

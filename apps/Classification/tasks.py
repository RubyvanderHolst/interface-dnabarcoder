from apps.Cutoff.tasks import bytes_to_larger, send_results_email, add_task_to_db
from apps.Authentication.models import TaskInfo

from django.conf import settings
from django.contrib.auth.models import User

from celery import shared_task
import pandas as pd
import os
import secrets

base_dir = settings.BASE_DIR
dnabarcoder_path = os.popen("find /home -name dnabarcoder.py").read().rstrip('\n')


@shared_task
def classify_blast(input_sequences_path, reference_path,
                   num_cutoff, file_cutoff_path,
                   min_alignment_length, confidence, min_group_number,
                   min_seq_number, rank, output_dir, email):
    # Celery task for classification with BLAST

    task_id = classify_blast.request.id
    os.system(f'cd {output_dir} && mkdir {task_id}')
    output_dir = os.path.join(output_dir, task_id)

    # calculate best matches
    prefix = os.path.basename(input_sequences_path).split('.')[0] + "." + \
             os.path.basename(reference_path).split('.')[0]
    command_search = f"python {dnabarcoder_path} search " \
                     f"--input {input_sequences_path} " \
                     f"--reference {reference_path} " \
                     f"--minalignmentlength {min_alignment_length} " \
                     f"--out {output_dir} "
    os.system(command_search)

    # classify based on the best matches
    classify_input = None
    for file in os.listdir(output_dir):
        if file.endswith(".bestmatch"):
            classify_input = os.path.join(output_dir, file)
            break
    command_classify = f"python {dnabarcoder_path} classify " \
                       f"--input {classify_input} " \
                       f"--reference {reference_path} " \
                       f"-prefix {prefix} " \
                       f"--minalignmentlength {min_alignment_length} " \
                       f"--out {output_dir} "
    #                  f"--minproba {min_probability} " \
    #                  f"--maxseqno {max_seq_number} " \
    if rank != "":
        command_classify += f"-rank {rank} "

    # Global cutoff
    if num_cutoff is not None:
        command_classify += f"--globalcutoff {num_cutoff} "
        if confidence != "":
            command_classify += f"--globalconfidence {confidence} "
    # Local cutoffs
    else:
        command_classify += f"-cutoffs {file_cutoff_path} " \
                            f"-minseqno {min_seq_number} " \
                            f"-mingroupno {min_group_number} "

    os.system(command_classify)

    # Remove blast db files
    os.system(f"cd {'/'.join(reference_path.split('/')[:-1])} && "
              f"find -type f -name '*.blastdb.*' -delete")

    dict_files = get_file_sizes(output_dir)

    # Check if results file has result
    result_file = None
    for file in dict_files.keys():
        if file.endswith('.classified'):
            result_file = file
    if result_file is not None:
        has_results = check_results_generated(os.path.join(output_dir,
                                                           result_file))
    else:
        has_results = False

    os.remove(input_sequences_path)
    if 'media/uploaded' in reference_path:
        os.remove(reference_path)

    if file_cutoff_path is not None:
        os.remove(file_cutoff_path)

    if email is not None and email != '':
        password = add_task_to_db(task_id, 'classification', email)
        send_results_email('http://localhost:8000', 'classification', task_id,
                           email, password)

    return dict_files, has_results


def get_file_sizes(dir_path):
    # Get the sizes of all files in a directory
    # Return dictionary: {file_name: file_size}
    file_list = os.listdir(dir_path)
    dict_files = {}
    for name in file_list:
        if name[0] != '.':
            size = bytes_to_larger(
                os.stat(os.path.join(dir_path, name)).st_size)
            dict_files[name] = size
    return dict_files


def check_results_generated(result_file):
    # Checks if column "Prediction" in a tab seperated file is empty
    # Return a boolean
    data_results = pd.read_csv(result_file, sep='\t')
    df_results = pd.DataFrame(data_results, columns=['Prediction'])
    if df_results['Prediction'].isnull().all():
        return False
    else:
        return True

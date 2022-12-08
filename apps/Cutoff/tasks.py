from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from celery import shared_task
import pandas as pd
from Bio import SeqIO
import os


base_dir = settings.BASE_DIR
dnabarcoder_path = os.popen("find /home -name dnabarcoder.py").read().rstrip('\n')


@shared_task
def calculate_cutoff(input_file_path, sim_file_path,
                     min_alignment_length, rank, higher_rank,
                     starting_threshold, end_threshold, step, min_group_number,
                     min_seq_number, max_seq_number, remove_comp, prefix,
                     output_dir, email):
    # Celery task for cutoff calculation

    task_id = calculate_cutoff.request.id
    os.system(f'cd {output_dir} && mkdir {task_id}')
    output_dir = os.path.join(output_dir, task_id)

    # Removal of similar sequences
    # dict_similar = None
    # if threshold is not None:
    #     remove_complexes(dnabarcoder_path, input_file_path, threshold,
    #                      min_alignment_length, rank, output_dir, sim_file_path)
    #     original_input_file_path = f"{input_file_path}"
    #     input_file_path = os.path.join(output_dir,
    #                                    input_file_path.split('/')[-1].replace('fasta', 'diff.fasta'))
    #     dict_similar = get_removed_complexes(prefix, output_dir)

    command = f"python {dnabarcoder_path} " \
              f"predict " \
              f"--input {input_file_path} " \
              f"--minalignmentlength {min_alignment_length} " \
              f"-rank {rank} " \
              f"--startingthreshold {starting_threshold} " \
              f"--endthreshold {end_threshold} " \
              f"--step {step} " \
              f"-mingroupno {min_group_number} " \
              f"-minseqno {min_seq_number} " \
              f"-maxseqno {max_seq_number} " \
              f"-removecomplexes {remove_comp} " \
              f"-prefix {prefix} " \
              f"--out {output_dir} "

    # Local cutoff calculation
    if higher_rank is not None:
        command += f"-higherrank {higher_rank} "
    # If user gives similarity matrix
    if sim_file_path is not None:
        command += f"--simfilename {sim_file_path} "

    os.system(command)

    dict_files, dict_images = get_file_sizes(output_dir)

    # Check if results have been generated
    result_file = None
    for file in dict_files.keys():
        if file.endswith('.cutoffs.json.txt'):
            result_file = file
            break
    if result_file is not None:
        has_results = check_results_generated(os.path.join(output_dir,
                                                           result_file))
    else:
        has_results = False

    try:
        os.remove(original_input_file_path)
    except:
        os.remove(input_file_path)

    if sim_file_path is not None:
        os.remove(sim_file_path)

    if email is not None:
        send_results_email('http://localhost:8000', 'cutoff', task_id, email)

    return dict_files, dict_images, has_results


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
        elif name[0] != '.':
            dict_files[name] = size
    return dict_files, dict_images


def bytes_to_larger(size_b):
    # Convert byte sizes to larger sizes
    # Returns a string of the size
    sizes = ['TB', 'GB', 'MB', 'KB', 'B']
    x = 10**((len(sizes) - 1) * 3)
    for size in sizes:
        if size_b > x:
            return f"{int(size_b / x)} {size}"
        else:
            x *= 10**-3


def check_results_generated(result_file):
    # Checks if a file has more than one line
    # Return a boolean
    file = open(result_file, 'r')
    has_results = True
    print()
    if len(file.readlines()) < 2:
        has_results = False
    file.close()
    return has_results


def send_results_email(website_url, page, task_id, email):
    results_link = os.path.join(website_url, page, task_id)
    plain_message = 'Dear User,\n\n' \
                    'Your task has finished running.\n' \
                    f'Click the link to see your results: {results_link}'
    html_message = render_to_string('email_template.html', {
        'link_to_results': results_link,
        'link_to_website': website_url,
        'task_type': page,
    })
    if email is not None:
        print(f'Send email from {settings.EMAIL_HOST_USER} to {email}')
        send_mail(
            subject='DNAbarcoder task has finished',
            message=plain_message,
            html_message=html_message,
            from_email='r.holst@wi.knaw.nl',
            recipient_list=[email],
            fail_silently=False,
        )


# def remove_complexes(dnabarcoder_path, input_file_path, threshold,
#                      min_alignment_length, rank, output_dir, sim_file_path):
#     # Removal of similar sequences
#     command = f"python {dnabarcoder_path} "\
#               f"remove "\
#               f"--input {input_file_path} "\
#               f"--cutoff {threshold} "\
#               f"--minalignmentlength {min_alignment_length} "\
#               f"--classificationrank {rank} "\
#               f"--out {output_dir} "
#
#     if sim_file_path is not None:
#         command += f"--simfilename {sim_file_path} "
#
#     os.system(command)
#
#     os.system(f"cd {base_dir} && "
#               "rm db.n*")


# def get_removed_complexes(prefix, output_dir):
#     # Makes a dictionary of the removed/preserved sequences
#     # return dict: {num_cluster: {'representing': [list of ids from fasta],
#     #                             'removed': [list of ids from fasta]}}
#     similar_file = None
#     diff_fasta_file = None
#     for file_name in os.listdir(output_dir):
#         if file_name.endswith('.similar'):
#             similar_file = os.path.join(output_dir, prefix + '.similar')
#         elif file_name.endswith('.diff.fasta'):
#             diff_fasta_file = os.path.join(output_dir, prefix + '.diff.fasta')
#     data_similar = pd.read_csv(similar_file, sep='\t')
#     df_similar = pd.DataFrame(data_similar)
#
#     diff_fasta = SeqIO.parse(open(diff_fasta_file), 'fasta')
#     ids_in_fasta = [fasta.id for fasta in diff_fasta]
#
#     dict_similar = {}
#     for index, row in df_similar.iterrows():
#         cluster = row['ClusterID']
#         full_id = row['SequenceID']
#         classification = row['Classification']
#         simple_id = full_id.split(' ')[0]
#         if cluster not in dict_similar.keys():
#             dict_similar[cluster] = {'representing': [],
#                                      'removed': []}
#         if simple_id in ids_in_fasta:
#             dict_similar[cluster]['representing'].append(f"{simple_id} {classification}")
#         else:
#             dict_similar[cluster]['removed'].append(f"{simple_id} {classification}")
#
#     # Remove clusters with no removed sequences
#     final_dict_similar = {}
#     for cluster in dict_similar.keys():
#         if len(dict_similar[cluster]['removed']) != 0:
#             final_dict_similar[cluster] = dict_similar[cluster]
#
#     return final_dict_similar

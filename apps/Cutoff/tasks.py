from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from apps.Authentication.models import TaskInfo

from celery import shared_task
import pandas as pd
from Bio import SeqIO
import os
import secrets
import subprocess


base_dir = settings.BASE_DIR
media_url = settings.MEDIA_URL
dnabarcoder_path = os.popen("find /home -name dnabarcoder.py").read().rstrip('\n')


@shared_task
def calculate_cutoff(input_file_path, sim_file_path,
                     min_alignment_length, rank, higher_rank,
                     starting_threshold, end_threshold, step, min_group_number,
                     min_seq_number, max_seq_number, remove_comp, prefix,
                     output_dir, email):
    # Celery task for cutoff calculation

    task_id = calculate_cutoff.request.id
    subprocess.run(f'cd {output_dir} && mkdir {task_id}', shell=True, stdout=subprocess.DEVNULL)
    output_dir = os.path.join(output_dir, task_id)

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

    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

    html_files_table, files, dict_images = get_file_sizes(output_dir, task_id)

    # Check if results have been generated
    result_file = None
    for file in files:
        if file.endswith('.cutoffs.json.txt'):
            result_file = file
            break
    if result_file is not None:
        has_results = check_results_generated(os.path.join(output_dir,
                                                           result_file))
    else:
        has_results = False

    # Remove input files
    os.remove(input_file_path)
    if sim_file_path is not None:
        os.remove(sim_file_path)

    # Send email
    if email is not None and email != '':
        password = add_task_to_db(task_id, 'cutoff', email)
        send_results_email('http://localhost:8000', 'cutoff', task_id, email,
                           password)

    return html_files_table, dict_images, has_results


def get_file_sizes(dir_path, task_id):
    # Create a table of the result files
    # Table columns: file name, file size and download button
    # returns HTML table and list of file names

    file_list = os.listdir(dir_path)
    dict_files = {'File name': [], 'File size': [], 'Download': []}
    dict_images = {}
    for name in file_list:
        size = bytes_to_larger(os.stat(os.path.join(dir_path, name)).st_size)
        if os.path.splitext(name)[1] == '.png':
            dict_images[name] = size
        elif name[0] != '.':
            dict_files['File name'].append(name)
            dict_files['File size'].append(size)
            dict_files['Download'].append(
                f"<a href='{os.path.join(media_url, 'results', task_id, name)}' class='link-light text-decoration-none' download='{name}'>"
                f"<button type='button' class='btn btn-primary w-75'><i class='bi bi-download'></i> Download</button>"
                f"</a>"
            )

    if len(dict_files['File name']) == 0:
        html = None
    else:
        html = pd.DataFrame(dict_files).to_html(
            index=False,
            justify="left",
            border=0,
            classes="table table-striped table-hover",
        )
        html = html.replace('&lt;', '<').replace('&gt;', '>')
    return html, dict_files['File name'], dict_images


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


def send_results_email(website_url, page, task_id, email, password):
    # Send an email with log in instructions
    results_link = os.path.join(website_url, 'login')
    plain_message = 'Dear User,\n\n' \
                    'Your task has finished running.\n' \
                    f'Log in to see your results: {results_link}.\n' \
                    f'Your task ID is {task_id} \n' \
                    f'The password to this task is {password}'
    html_message = render_to_string('email_template.html', {
        'link_to_results': results_link,
        'link_to_website': website_url,
        'task_type': page,
        'task_id': task_id,
        'password': password,
    })
    if email is not None:
        print(f'Send email from {settings.EMAIL_HOST_USER} to {email}')
        send_mail(
            subject='DNAbarcoder task has finished',
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )


def add_task_to_db(task_id, task_type, email):
    # Add records for User and TaskInfo tables based on given info
    password = secrets.token_urlsafe(10)

    user = User.objects.create_user(
        username=task_id,
        email=email,
        password=password,
    )
    user.save()

    task_instance = TaskInfo(
        user=user,
        task_type=task_type,
    )
    task_instance.save()
    return password

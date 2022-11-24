from apps.Cutoff.tasks import bytes_to_larger
from apps.Cutoff.tasks import check_results_generated

from django.conf import settings

from celery import shared_task
import os

base_dir = settings.BASE_DIR
dnabarcoder_path = os.popen("find /home -name dnabarcoder.py").read().rstrip('\n')


@shared_task
def classify_blast(input_sequences_path, reference_path,
                   num_cutoff, file_cutoff_path,
                   min_alignment_length, confidence, min_group_number,
                   min_seq_number, rank, output_dir, input_dir):
    # Celery task for classification with BLAST

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
    classify_input = os.path.join(output_dir, prefix + '_BLAST.bestmatch')
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
        if file.endswith('.classification'):
            result_file = file
    if result_file is not None:
        has_results = check_results_generated(os.path.join(output_dir,
                                                           result_file))
    else:
        has_results = False

    os.system(f'rm {os.path.join(input_dir, "*")}')

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

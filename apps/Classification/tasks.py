from celery import shared_task
import os
import sys
if sys.version_info[0] >= 3:
   unicode = str
from apps.Cutoff.tasks import bytes_to_larger


@shared_task
def classify_blast(input_sequences_path, reference_path,
                   num_cutoff, file_cutoff_path,
                   min_alignment_length, confidence, min_group_number,
                   min_seq_number, rank, output_dir):
    # calculate best matches
    prefix = os.path.basename(input_sequences_path).split('.')[0] + "." + \
                        os.path.basename(reference_path).split('.')[0]
    command_search = f"python /home/tool/dnabarcoder.py search " \
                     f"--input {input_sequences_path} " \
                     f"--reference {reference_path} " \
                     f"--minalignmentlength {min_alignment_length} " \
                     f"--out {output_dir} "
    os.system(command_search)

    # classify based on the best matches
    classify_input = os.path.join(output_dir, prefix + '_BLAST.bestmatch')
    command_classify = f"python /home/tool/dnabarcoder.py classify " \
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
    return get_file_sizes(output_dir)


def get_file_sizes(dir_path):
    # Get the sizes of all files in a directory
    # Return dictionary: {file_name: file_size}
    file_list = os.listdir(dir_path)
    dict_files = {}
    for name in file_list:
        if name[0] != '.':
            size = bytes_to_larger(os.stat(os.path.join(dir_path, name)).st_size)
            dict_files[name] = size
    return dict_files


def convert_to_unicode():
    pass


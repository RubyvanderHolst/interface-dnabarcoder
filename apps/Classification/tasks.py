from celery import shared_task
import os


@shared_task
def classify_blast(input_sequences_path, reference_path,
                   num_cutoff, file_cutoff_path, min_probability,
                   min_alignment_length, confidence, min_group_number,
                   min_seq_number, rank, max_seq_number, output_dir):
    # calculate best matches
    command_search = f"python /home/tool/dnabarcoder.py search " \
                     f"--input {input_sequences_path} " \
                     f"--reference {reference_path} " \
                     f"--minalignmentlength {min_alignment_length} " \
                     f"--out {output_dir} "
    os.system(command_search)
    # TODO gives error:
    #  Error: (803.7) [makeblastdb] Blast-def-line-set.E.title
    #  Bad char [0xC3] in string at byte 123
    #  (waarschijnlijk ë)

    # classify based on the best matches
    return get_file_sizes(output_dir)


def get_file_sizes(dir_path):
    # Get the sizes of all files in a directory
    # Return dictionary: {file_name: file_size}
    file_list = os.listdir(dir_path)
    dict_files = {}
    for name in file_list:
        size = bytes_to_larger(os.stat(os.path.join(dir_path, name)).st_size)
        dict_files[name] = size
    return dict_files

from celery import shared_task
import os


@shared_task
def calculate_cutoff(dnabarcoder_path, input_file_path, sim_file_path,
                     min_alignment_length, rank, higher_rank,
                     starting_threshold,
                     end_threshold, step, min_group_number, min_seq_number,
                     max_seq_number, threshold, prefix, output_dir):

    rem_comp_1 = "no"
    if threshold == "1":
        rem_comp_1 = "yes"
    elif threshold is not None:
        remove_complexes(dnabarcoder_path, input_file_path, threshold,
                         min_alignment_length, rank, output_dir,
                         sim_file_path)

        input_file_path = output_dir + "/" + input_file_path.split('/')[-1].\
            replace('fasta', 'diff.fasta')

    command = f"python {dnabarcoder_path} " \
              f"predict " \
              f"--input {input_file_path} " \
              f"--simfilename {sim_file_path} " \
              f"--minalignmentlength {min_alignment_length} " \
              f"-rank {rank} " \
              f"-higherrank {higher_rank} " \
              f"--startingthreshold {starting_threshold} " \
              f"--endthreshold {end_threshold} " \
              f"--step {step} " \
              f"-mingroupno {min_group_number} " \
              f"-minseqno {min_seq_number} " \
              f"-maxseqno {max_seq_number} " \
              f"-removecomplexes {rem_comp_1} " \
              f"-prefix {prefix} " \
              f"--out {output_dir} "

    os.system(command)

    dict_files, dict_images = get_file_sizes(output_dir)

    return dict_files, dict_images


def remove_complexes(dnabarcoder_path, input_file_path, threshold,
                     min_alignment_length, rank, output_dir, sim_file_path):
    command = f"python {dnabarcoder_path} "\
              f"remove "\
              f"--input {input_file_path} "\
              f"--cutoff {threshold} "\
              f"--minalignmentlength {min_alignment_length} "\
              f"--classificationrank {rank} "\
              f"--out {output_dir} "

    if sim_file_path is not None:
        command += f"--simfilename {sim_file_path} "

    os.system(command)


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
        else:
            dict_files[name] = size
    return dict_files, dict_images


def bytes_to_larger(size_b):
    sizes = ['TB', 'GB', 'MB', 'KB', 'B']
    x = 10**((len(sizes) - 1) * 3)
    for size in sizes:
        if size_b > x:
            return f"{int(size_b / x)} {size}"
        else:
            x *= 10**-3

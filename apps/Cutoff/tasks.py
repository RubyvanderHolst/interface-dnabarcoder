from celery import shared_task
import pandas as pd
from Bio import SeqIO
import os


@shared_task
def calculate_cutoff(dnabarcoder_path, input_file_path, sim_file_path,
                     min_alignment_length, rank, higher_rank,
                     starting_threshold, end_threshold, step, min_group_number,
                     min_seq_number, max_seq_number, threshold, prefix,
                     output_dir):

    dict_similar = None
    if threshold is not None:
        remove_complexes(dnabarcoder_path, input_file_path, threshold,
                         min_alignment_length, rank, output_dir, sim_file_path)
        input_file_path = os.path.join(output_dir,
                                       input_file_path.split('/')[-1].replace('fasta', 'diff.fasta'))
        dict_similar = get_removed_complexes(prefix, output_dir)

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
              f"-prefix {prefix} " \
              f"--out {output_dir} "

    if higher_rank is not None:
        command += f"-higherrank {higher_rank} "
    if sim_file_path is not None:
        command += f"--simfilename {sim_file_path} "

    os.system(command)
    # for key in dict_similar:
    #     print(f"{key}: {len(dict_similar[key]['representing'])}, {len(dict_similar[key]['removed'])}")

    dict_files, dict_images = get_file_sizes(output_dir)

    return dict_files, dict_images, dict_similar


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

    os.system("cd /home/app/ && "
              "rm db.n*")


def get_removed_complexes(prefix, output_dir):
    # return dict: {num_cluster: {'representing': [list of id's],
    #                             'removed': [list of id's]}}
    similar_file = None
    diff_fasta_file = None
    for file_name in os.listdir(output_dir):
        if file_name.endswith('.similar'):
            similar_file = os.path.join(output_dir, prefix + '.similar')
        elif file_name.endswith('.diff.fasta'):
            diff_fasta_file = os.path.join(output_dir, prefix + '.diff.fasta')
    data_similar = pd.read_csv(similar_file, sep='\t')
    df_similar = pd.DataFrame(data_similar)

    diff_fasta = SeqIO.parse(open(diff_fasta_file), 'fasta')
    ids_in_fasta = [fasta.id for fasta in diff_fasta]

    dict_similar = {}
    for index, row in df_similar.iterrows():
        cluster = row['ClusterID']
        full_id = row['SequenceID']
        classification = row['Classification']
        simple_id = full_id.split(' ')[0]
        if cluster not in dict_similar.keys():
            dict_similar[cluster] = {'representing': [],
                                     'removed': []}
        if simple_id in ids_in_fasta:
            dict_similar[cluster]['representing'].append(f"{simple_id} {classification}")
        else:
            dict_similar[cluster]['removed'].append(f"{simple_id} {classification}")

    # Remove clusters with no removed sequences
    final_dict_similar = {}
    for cluster in dict_similar.keys():
        if len(dict_similar[cluster]['removed']) != 0:
            final_dict_similar[cluster] = dict_similar[cluster]

    return final_dict_similar
    

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
    sizes = ['TB', 'GB', 'MB', 'KB', 'B']
    x = 10**((len(sizes) - 1) * 3)
    for size in sizes:
        if size_b > x:
            return f"{int(size_b / x)} {size}"
        else:
            x *= 10**-3

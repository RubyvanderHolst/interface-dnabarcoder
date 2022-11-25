from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
import os


base_dir = settings.BASE_DIR


# Form for classification input
class ClassificationForm(forms.Form):
    file_input_sequences = forms.FileField(
        label='Select a FASTA file',
        widget=forms.FileInput(
            attrs={'accept': ".fasta,.fna,.ffn,.faa,.frn,.fa"}
        )
    )
    text_input_sequences = forms.CharField(
        label='Or paste the sequences',
        widget=forms.Textarea(attrs={
            'placeholder': """>ID_12345
TTAAATAATCAATAATCTTGGCTTGTCCATTATTATCTATTTACTGTGAACTGTATTATT
ATTTGACGTTTGAGGGATGTTCCAATGTTATAAGGATAGACATTGGAAATGTTAACCGAG
TCATAATCAGGTTTAGGCCTGGTATCCTATTATTATTTACCAAATGAATTCAGAATTAAT
ATTGTAACATAGACCTAAAAAATCTATAAAACAACTTTTAACAACGGATCTCTTGGTTCT
CGCATCGATGAAGAACGTAGCAAAGTGCGATAACTAGTGTGAATTGCATATTCAGTGAAT
CATCGAGTCTTTGAACGCAACTTGCGCTCATTGGTATTCCAATGAGCACGCCTGTTTCAG
TATCAAAACAAACCCTCTATTCAACTTTTGTTGTATAGGATTATTGGGGGCCTCTCGATC
TGTATAGATCTTGAAACCCTTGAAATTTACTAAGGCCTGAACTTGTTTAATGCCTGAACT
TTTTTTTAATATAAAGGAAAGCTCTTGTAATTGACTTTGATGGGGCCTCCCAAATAAATC
TCTTTTAAATTTGATCTGAAATCAGG
""",
            'rows': 10,
            'class': "w-475"
        })
    )

    path = os.path.join(base_dir, "reference_files")
    list_files = os.listdir(path)
    reference_choices = [('', 'Use own file')]
    for file in list_files:
        reference_choices.append((file, file))
    reference_options = forms.CharField(
        label='Choose a reference file:',
        widget=forms.Select(
            choices=reference_choices
        ),
        required=False,
    )
    input_reference = forms.FileField(
        label='Select a reference file (FASTA)',
        widget=forms.FileInput(
            attrs={'accept': ".fasta,.fna,.ffn,.faa,.frn,.fa"}
        )
    )

    cutoff_type = forms.CharField(
        label='Type of similarity cutoff',
        widget=forms.RadioSelect(
            choices=[('local', 'Local'),
                     ('global', 'Global')]),
        initial='local',
    )
    num_cutoff = forms.FloatField(
        label='Global cutoff value',
        widget=forms.NumberInput(attrs={
            'min': 0,
            'max': 1,
        }),
        required=False,
    )
    file_cutoff = forms.FileField(
        label='Local cutoff file',
        widget=forms.FileInput(
            attrs={'accept': ".json"}
        )
    )

    # min_probability = forms.FloatField(
    #     label='Minimum probability of similarity cutoff',
    #     widget=forms.NumberInput(attrs={
    #         'min': 0,
    #         'max': 1,
    #     }),
    #     required=False,
    # )
    min_alignment_length = forms.IntegerField(
        label='Minimum sequence alignment length',
        widget=forms.NumberInput(attrs={
            'min': 1,
        }),
        initial=400,
    )
    confidence = forms.FloatField(
        label='Confidence of the global similarity cutoff',
        widget=forms.NumberInput(attrs={
            'min': 0,
            'max': 1,
            'disabled': True,
        }),
        required=False,
    )
    min_group_number = forms.IntegerField(
        label='Minimum number of groups for prediction',
        widget=forms.NumberInput(attrs={
            'min': 1,
        }),
        initial=5,
    )
    min_seq_number = forms.IntegerField(
        label='Minimum number of sequences for prediction',
        widget=forms.NumberInput(attrs={
            'min': 1,
        }),
        initial=50,
    )
    rank = forms.CharField(
        label='Rank:',
        widget=forms.Select(
            choices=[('', ''),
                     ('species', 'Species'),
                     ('genus', 'Genus'),
                     ('family', 'Family'),
                     ('order', 'Order'),
                     ('class', 'Class'),
                     ('phylum', 'Phylum'),
                     ('kingdom', 'Kingdom')]
        ),
        required=False,
    )
    # max_seq_number = forms.IntegerField(
    #     label='Maximum number of sequences per taxon name for best match determination',
    #     widget=forms.NumberInput(attrs={
    #         'min': 1,
    #     }),
    #     required=False,
    # )

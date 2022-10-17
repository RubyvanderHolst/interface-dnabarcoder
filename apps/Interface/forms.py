from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
import os

class CutoffForm(forms.Form):
    input_file = forms.FileField(
        label='Select a FASTA file',
        widget=forms.FileInput(
            attrs={'accept': ".fasta,.fna,.ffn,.faa,.frn,.fa"}
        )
    )
    cutoff_type = forms.CharField(
        label='Local or global cutoff calculation',
        widget=forms.RadioSelect(
            choices=[('local', 'Local'),
                     ('global', 'Global')]),
        initial='local',
    )
    rank = forms.CharField(
        label='Identification rank',
        widget=forms.Select(
            choices=[('species', 'Species'),
                     ('genus', 'Genus'),
                     ('family', 'Family'),
                     ('order', 'Order'),
                     ('class', 'Class'),
                     ('phylum', 'Phylum'),
                     ('kingdom', 'Kingdom')]
        )
    )
    higher_rank = forms.CharField(
        label='Higher rank',
        widget=forms.Select(
            choices=[('species', 'Species'),
                     ('genus', 'Genus'),
                     ('family', 'Family'),
                     ('order', 'Order'),
                     ('class', 'Class'),
                     ('phylum', 'Phylum'),
                     ('kingdom', 'Kingdom')]
        ),
        initial=('genus', 'Genus'),
    )
    sim_file = forms.FileField(
        label='Select a similarity matrix file:',
        widget=forms.FileInput(),
        required=False,
    )
    min_group_number = forms.IntegerField(
        label='Minimum number of groups for prediction:',
        validators=[MinValueValidator(0)],
        initial=5,
    )
    min_alignment_length = forms.IntegerField(
        label='Minimum sequence alignment length:',
        validators=[MinValueValidator(0)],
        initial=400,
    )
    min_seq_number = forms.IntegerField(
        label='Minimum number of sequences for prediction:',
        validators=[MinValueValidator(0)],
        initial=50,
    )

    starting_threshold = forms.FloatField(
        label='Starting threshold',
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        initial=0.7,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    end_threshold = forms.FloatField(
        label='Ending threshold',
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    step = forms.FloatField(
        label='Step size',
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        initial=0.001,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    max_seq_number = forms.IntegerField(
        label='Maximum number of sequences per taxon name:',
        validators=[MinValueValidator(0)],
        initial=20000,
    )

    remove_comp = forms.BooleanField(
        label='Remove sequences of the same complexes',
        widget=forms.CheckboxInput(attrs={'class': "form-check-input"}),
        required=False,
    )
    cutoff_remove = forms.FloatField(
        label='Similarity cut-off for removal:',
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        initial=1,
        disabled=True,
    )


class ClassificationForm(forms.Form):
    file_input_sequences = forms.FileField(
        label='Select a FASTA file:',
        widget=forms.FileInput(
            attrs={'accept': ".fasta,.fna,.ffn,.faa,.frn,.fa"}
        )
    )
    text_input_sequences = forms.CharField(
        label='Or paste the sequences:',
        widget=forms.Textarea(attrs={
            'placeholder': """>ID k__kingdom;p__phylum;c__class;o__order;f__family;g__genus;s__species
TCGTAACAAGGTCTCCGTTGGTGAACCAGCGGAGGGATCATTACCGAGTTTACAACTCCC
AAACCCCTGTGAACATACCTATACGTTGCCTCGGCGGATCAGCCCGCGCCCCGTAAAACG
GGACGGCCCGCCCGAGGACCCTAAACTCTGTTTTTAGTGGAACTTCTGAGTAAAACAAAC
""",
            'rows': 5,
        })
    )

    path = "/home/app/data"
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
        label='Select a reference file (FASTA):',
        widget=forms.FileInput(
            attrs={'accept': ".fasta,.fna,.ffn,.faa,.frn,.fa"}
        )
    )

    cutoff_type = forms.CharField(
        label='Type of similarity cutoff:',
        widget=forms.RadioSelect(
            choices=[('local', 'Local'),
                     ('global', 'Global')]),
        initial='local',
    )
    num_cutoff = forms.FloatField(
        label='Global cutoff value:',
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        required=False,
    )
    file_cutoff = forms.FileField(
        label='Local cutoff file:',
        widget=forms.FileInput(
            attrs={'accept': ".json"}
        )
    )

    min_probability = forms.FloatField(
        label='Minimum probability of similarity cutoff:',
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        required=False,
    )
    min_alignment_length = forms.IntegerField(
        label='Minimum sequence alignment length:',
        validators=[MinValueValidator(0)],
        initial=400,
    )
    confidence = forms.FloatField(
        label='Confidence of the similarity cutoff:',
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        required=False,
    )
    min_group_number = forms.IntegerField(
        label='Minimum number of groups for prediction:',
        validators=[MinValueValidator(0)],
        initial=5,
    )
    min_seq_number = forms.IntegerField(
        label='Minimum number of sequences for prediction:',
        validators=[MinValueValidator(0)],
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
    max_seq_number = forms.IntegerField(
        label='Maximum number of sequences per taxon name for best match determination:',
        validators=[MinValueValidator(0)],
        required=False,
    )

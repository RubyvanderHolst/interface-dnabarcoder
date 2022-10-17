from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


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





from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


# Form for cutoff input
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
                     ('kingdom', 'Kingdom'),
                     ('all', 'All')]
        )
    )
    higher_rank = forms.CharField(
        label='Higher rank',
        widget=forms.Select(
            choices=[('genus', 'Genus'),
                     ('family', 'Family'),
                     ('order', 'Order'),
                     ('class', 'Class'),
                     ('phylum', 'Phylum'),
                     ('kingdom', 'Kingdom'),
                     ('all', 'All')]
        ),
        initial=('genus', 'Genus'),
    )
    sim_file = forms.FileField(
        label='Select a similarity matrix file',
        widget=forms.FileInput(),
        required=False,
    )
    min_group_number = forms.IntegerField(
        label='Minimum number of groups for prediction',
        widget=forms.NumberInput(
            attrs={
                'min': 1,
            }
        ),
        initial=5,
    )
    min_alignment_length = forms.IntegerField(
        label='Minimum sequence alignment length',
        widget=forms.NumberInput(
            attrs={
                'min': 1,
            }
        ),
        initial=400,
    )
    min_seq_number = forms.IntegerField(
        label='Minimum number of sequences for prediction',
        widget=forms.NumberInput(
            attrs={
                'min': 1,
            }
        ),
        initial=50,
    )

    starting_threshold = forms.FloatField(
        label='Starting threshold',
        initial=0.7,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'max': 1,
        })
    )
    end_threshold = forms.FloatField(
        label='Ending threshold',
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'max': 1,
        })
    )
    step = forms.FloatField(
        label='Step size',
        initial=0.001,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0.00001,
            'max': 0.1,
        })
    )

    max_seq_number = forms.IntegerField(
        label='Maximum number of sequences per prediction',
        widget=forms.NumberInput(attrs={
            'min': 1,
        }),
        initial=20000,
    )

    remove_comp = forms.BooleanField(
        label='Remove sequences of the same complexes',
        widget=forms.CheckboxInput(attrs={
            'class': "form-check-input"
        }),
        required=False,
    )

    email = forms.EmailField(
        label='Send email when finished:',
        min_length=5,
        max_length=200,
        required=False,
    )



function cutoff_input_change() {
    let button_checked = document.querySelector('input[name=type_cutoff]:checked').value;

    if (button_checked === "global_cutoff") {
        document.getElementById('div_num_cutoff').style.display = "block";
        document.getElementById('file_cutoff').style.display = "none";
    } else {
        document.getElementById('div_num_cutoff').style.display = "none";
        document.getElementById('file_cutoff').style.display = "block";
    }

    switch_required_cutoff()
}

function switch_required_cutoff() {
    const inputs = [document.getElementById('num_cutoff'),
        document.getElementById('file_cutoff')]
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].required = !inputs[i].required
    }
}

function show_ref_file_input(dropdown) {
    if (dropdown.value === "") {
        document.getElementById('div_file_input_reference').style.display = "block";
        document.getElementById('input_reference').required = true;
    } else {
        document.getElementById('div_file_input_reference').style.display = "none";
        document.getElementById('input_reference').required = false;
        document.getElementById('input_reference').value = '';
    }
}


// Checks if one of sequence file inputs has input
document.addEventListener('DOMContentLoaded', function() {
    const inputs = Array.from(
        document.querySelectorAll('#file_input_sequences, #text_input_sequences')
    );
    console.log(inputs)
    const inputListener = e => {
        inputs
          .filter(i => i !== e.target)
          .forEach(i => (i.required = false));
    };

    inputs.forEach(i => i.addEventListener('input', inputListener));
});

document.addEventListener('DOMContentLoaded', function() {
    // Show/hide reference file input
    let reference_dropdown = document.getElementById('id_reference_options')
    reference_dropdown.addEventListener('change', function() {
        if (reference_dropdown.value === "") {
            document.getElementById('div_file_input_reference').style.display = "block";
            document.getElementById('id_input_reference').required = true;
        } else {
            document.getElementById('div_file_input_reference').style.display = "none";
            document.getElementById('id_input_reference').required = false;
            document.getElementById('id_input_reference').value = '';
        }
    })

    // Switch between number and file input for cutoff
    let cutoff_radio = Array.from(
        document.querySelectorAll('input[name="cutoff_type"]')
    )
    let cutoff_inputs = [document.getElementById('id_num_cutoff'),
                         document.getElementById('id_file_cutoff')]

    for (let i = 0; i < cutoff_radio.length; i++) {
        let radiobutton = cutoff_radio[i]
        radiobutton.addEventListener('click', function () {
            let button_checked = document.querySelector('input[name=cutoff_type]:checked').value;
            if (button_checked === "global") {
                document.getElementById('div_num_cutoff').style.display = "block";
                document.getElementById('div_file_cutoff').style.display = "none";
                document.getElementById('id_file_cutoff').value = '';
            } else {
                document.getElementById('div_num_cutoff').style.display = "none";
                document.getElementById('div_file_cutoff').style.display = "block";
            }
            for (let i = 0; i < cutoff_inputs.length; i++) {
                cutoff_inputs[i].required = !cutoff_inputs[i].required
            }
        })
    }

    // Check if one of unidentified sequences has input
    const inputs = Array.from(
        document.querySelectorAll('#id_file_input_sequences, #id_text_input_sequences')
    );
    const inputListener = e => {
        inputs
          .filter(i => i !== e.target)
          .forEach(i => (i.required = false));
    };

    inputs.forEach(i => i.addEventListener('input', inputListener));
});
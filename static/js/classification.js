//TODO change display change to class change
document.addEventListener('DOMContentLoaded', function() {
    // empty file or textarea input when other is filled in (seq input)
    let seq_file_input = document.getElementById('id_file_input_sequences')
    let seq_text_input = document.getElementById('id_text_input_sequences')
    seq_file_input.addEventListener('input', function() {
        seq_text_input.value = ''
    })
    seq_text_input.addEventListener('input', function() {
        seq_file_input.value = ''
    })

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

                document.getElementById('id_confidence').disabled = false;
                // TODO make empty?
                document.getElementById('id_min_seq_number').disabled = true;
                document.getElementById('id_min_seq_number').required = false;

                document.getElementById('id_min_group_number').disabled = true;
                document.getElementById('id_min_group_number').required = false;
            } else {
                document.getElementById('div_num_cutoff').style.display = "none";
                document.getElementById('div_file_cutoff').style.display = "block";

                document.getElementById('id_confidence').disabled = true;
                // TODO make empty?
                document.getElementById('id_min_seq_number').disabled = false;
                document.getElementById('id_min_seq_number').required = true;

                document.getElementById('id_min_group_number').disabled = false;
                document.getElementById('id_min_group_number').required = true;
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


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

function single_checkbox(checkbox) {
    if (checkbox.checked === true) {
        // Select all checkboxes by class
        deselect_standard()
        checkbox.checked = true; // Checked clicked checkbox

        // empty reference file input
        document.getElementById('input_reference').value = null;
    }
}

function deselect_standard() {
    let checkboxesList = document.getElementsByClassName("form-check-input");
        for (let i = 0; i < checkboxesList.length; i++) {
            checkboxesList.item(i).checked = false; // Uncheck all checkboxes
        }
}

// Checks if one of reference file input or checkboxes has input
document.addEventListener('DOMContentLoaded', function() {
  const inputs = Array.from(
    document.querySelectorAll('input[class=form-check-input], input[id=input_reference]')
  );

  const inputListener = e => {
    inputs
      .filter(i => i !== e.target)
      .forEach(i => (i.required = !e.target.value.length));
  };

  inputs.forEach(i => i.addEventListener('input', inputListener));
});
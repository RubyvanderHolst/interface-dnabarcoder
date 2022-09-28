

function switch_home_settings(button) {
    if (button.id === "home_button") {
        button.classList.add("active");
        document.getElementById("settings_button").classList.remove("active");

        console.log("home", button.classList)
        console.log("settings", document.getElementById("settings_button").classList)

        document.getElementById("classification_home").style.display = "block";
        document.getElementById("classification_settings").style.display = "none";
    } else if (button.id === "settings_button") {
        document.getElementById("home_button").classList.remove("active");
        button.classList.add("active");

        console.log("settings", button.classList)
        console.log("home", document.getElementById("settings_button").classList)

        document.getElementById("classification_home").style.display = "none";
        document.getElementById("classification_settings").style.display = "block";
    }
}


function tax_input_change(bool_show) {
    // Show or hide taxonomy input file based on var_show.
    // This can be "none" (hidden) or "block" (show).
    let var_show
    if (bool_show) {
        var_show = 'block'
    } else {
        var_show = 'none'
    }
    document.getElementById('input_tax').style.display = var_show;
    document.getElementById('input_tax').required = bool_show;
}

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
    let checkboxesList = document.getElementsByClassName("checkoption");
        for (let i = 0; i < checkboxesList.length; i++) {
            checkboxesList.item(i).checked = false; // Uncheck all checkboxes
        }
}

// Checks if one of reference file input or checkboxes has input
document.addEventListener('DOMContentLoaded', function() {
  const inputs = Array.from(
    document.querySelectorAll('input[class=checkoption], input[id=input_reference]')
  );

  const inputListener = e => {
    inputs
      .filter(i => i !== e.target)
      .forEach(i => (i.required = !e.target.value.length));
  };

  inputs.forEach(i => i.addEventListener('input', inputListener));
});
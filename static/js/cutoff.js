// Keep in mind that cutoff.html also uses functions from classification.js

// duplicate from classification.js
function tax_input_change(bool_show) {
    // Show or hide taxonomy input file based on var_show.
    // This can be "none" (hidden) or "block" (show).
    let var_show
    if (bool_show) {
        var_show = 'block'
    } else {
        var_show = 'none'
    }
    document.getElementById('file_input_tax').style.display = var_show;
    document.getElementById('file_input_tax').required = bool_show;
}


function disable_rank(clicked_radio) {
    // Disables higher rank checkboxes
    let checkboxes_list_higher = document.getElementsByClassName("checks_higher_rank");
    let checkboxes_list = document.getElementsByClassName("checks_rank")

    let checkboxes_to_disable
    let checkboxes_to_enable
    if (clicked_radio.id === 'local_choice') {
        checkboxes_to_disable = checkboxes_list
        checkboxes_to_enable = checkboxes_list_higher
    } else if (clicked_radio.id === 'global_choice'){
        checkboxes_to_disable = checkboxes_list_higher
        checkboxes_to_enable = checkboxes_list
    }

    for (let i = 0; i < checkboxes_to_disable.length; i++) {
        checkboxes_to_disable.item(i).checked = false;
        checkboxes_to_disable.item(i).disabled = true;
    }
    for (let i = 0; i < checkboxes_to_enable.length; i++) {
        checkboxes_to_enable.item(i).disabled = false;
    }

    if (document.getElementById('species').disabled) {
        document.getElementById('species').checked = true;
    } else {
        document.getElementById('species').checked = false;
    }
}

function disable_field(checkbox, field_id) {
    // Enable field when checkbox is checked (used for remove complexes)
    if (checkbox.checked) {
        document.getElementById(field_id).disabled = false;
    } else {
        document.getElementById(field_id).disabled = true;
    }
}


// Checks if one of the enabled rank checkboxes has input
document.addEventListener('DOMContentLoaded', function() {
    let checkboxes_all = Array.from(
        document.querySelectorAll('input[class="form-check-input checks_rank"],' +
            'input[class="form-check-input checks_higher_rank"]')
    )
    const inputListener = e => {
        checkboxes_all
            .filter(i => i !== e.target)
            .forEach(i => (i.required = false))
    };
    checkboxes_all.forEach(i => i.addEventListener('transitionend', inputListener));
    checkboxes_all.forEach(i => i.addEventListener('input', inputListener));
})




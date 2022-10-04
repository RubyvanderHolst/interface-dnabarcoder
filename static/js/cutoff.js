

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
        document.getElementById('species').checked = true;
    }
}

function disable_field(checkbox, field_id) {
    // Enable field when checkbox is checked (used for remove complexes)
    document.getElementById(field_id).disabled = !checkbox.checked;
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
                 .filter(i => i.disabled === false)
                 .forEach(i => (i.required = !e.target.value.length));
         };
    checkboxes_all.forEach(i => i.addEventListener('input', inputListener));
})




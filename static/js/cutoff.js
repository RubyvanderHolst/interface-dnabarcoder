
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
    document.getElementById('species').checked = true;
    for (let i = 0; i < checkboxes_to_enable.length; i++) {
        checkboxes_to_enable.item(i).disabled = false;
    }
}


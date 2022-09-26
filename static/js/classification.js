function tax_input_change(var_show) {
    // Show or hide taxonomy input file based on var_show.
    // This can be "none" (hidden) or "block" (show).
    document.getElementById('input_tax').style.display = var_show;
}

function cutoff_input_change() {
    let button_checked = document.querySelector('input[name=type_cutoff]:checked').value;

    if (button_checked === "global_cutoff") {
        document.getElementById('num_cutoff').style.display = "block";
        document.getElementById('file_cutoff').style.display = "none";
    } else {
        document.getElementById('num_cutoff').style.display = "none";
        document.getElementById('file_cutoff').style.display = "block";
    }
}
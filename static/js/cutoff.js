

function disable_rank(clicked_radio) {
    // Disables higher rank dropdown and shows/hides kingdom in rank
    let rank = document.getElementById('rank')
    let higher_rank = document.getElementById('higher_rank')

    if (clicked_radio.id === 'local_choice') {
        higher_rank.disabled = false;
        document.getElementById('kingdom_rank').hidden = true;
    } else if (clicked_radio.id === 'global_choice'){
        higher_rank.disabled = true;
        higher_rank.value = "";
        document.getElementById('kingdom_rank').hidden = false;
    }
}

function hide_higher_options() {
    // Hides higher rank option that are the same or lower than the selected rank
    if (!document.getElementById('higher_rank').disabled) {
        let all_rank = ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']
        let selected_rank = document.getElementById('rank').value
        let index = all_rank.findIndex(object => {
            return object === selected_rank
        })
        document.getElementById('higher_rank').value = all_rank[index + 1]
        for (let i = 1; i < index + 1; i++) {
            document.getElementById(all_rank[i] + "_higher").hidden = true;
        }
        for (let i = index + 1; i < all_rank.length; i++) {
            document.getElementById(all_rank[i] + "_higher").hidden = false;
        }
    }
}

function disable_field(checkbox, field_id) {
    // Enable field when checkbox is checked (used for remove complexes)
    document.getElementById(field_id).disabled = !checkbox.checked;
}





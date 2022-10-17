
document.addEventListener('DOMContentLoaded', function() {
    // Enable/disable higher rank
    let cutoff_radio = Array.from(
        document.querySelectorAll('input[name="cutoff_type"]')
    )
    let higher_rank_dropdown = document.getElementById('id_higher_rank')
    for (let i = 0; i < cutoff_radio.length; i++) {
        let radiobutton = cutoff_radio[i]
        radiobutton.addEventListener('click', function () {
            if (radiobutton.value === 'local') {
                higher_rank_dropdown.disabled = false;
            } else if (radiobutton.value === 'global') {
                higher_rank_dropdown.disabled = true;
                higher_rank_dropdown.value = "";
            }
        })
    }

    // Hide higher rank option that are the same or lower than the selected rank
    let rank_dropdown = document.getElementById('id_rank')
    rank_dropdown.addEventListener('change', function() {
        if (!higher_rank_dropdown.disabled) {
            let all_rank = ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']
            let selected_rank = rank_dropdown.value
            let index = all_rank.findIndex(object => {
                return object === selected_rank
            })

            if (index === all_rank.length-1) {
                higher_rank_dropdown.value = all_rank[index]
            } else {
                higher_rank_dropdown.value = all_rank[index + 1]
            }

            for (let i = 0; i < index; i++) {
                higher_rank_dropdown[i].hidden = true
            }
            for (let i = index; i < all_rank.length; i++) {
                higher_rank_dropdown[i].hidden = false
            }
        }
    })

    // Enable/disable cutoff_remove field based on remove_comp field
    let remove_comp_check = document.getElementById('id_remove_comp')
    remove_comp_check.addEventListener('change', function() {
        document.getElementById('id_cutoff_remove').disabled = !remove_comp_check.checked
    })
})
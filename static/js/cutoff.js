
document.addEventListener('DOMContentLoaded', function() {
    // Enable/disable higher rank
    let rank_dropdown = document.getElementById('id_rank')
    let higher_rank_dropdown = document.getElementById('id_higher_rank')
    let all_rank = ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']
    let cutoff_radio = Array.from(
        document.querySelectorAll('input[name="cutoff_type"]')
    )
    // Hide highest rank (Kingdom) (hidden for local cutoff)
    rank_dropdown[rank_dropdown.length-2].hidden = true

    // Hide All option rank (hidden for local cutoff)
    rank_dropdown[rank_dropdown.length-1].hidden = true

    for (let i = 0; i < cutoff_radio.length; i++) {
        let radiobutton = cutoff_radio[i]
        radiobutton.addEventListener('click', function () {
            if (radiobutton.value === 'local') {
                higher_rank_dropdown.disabled = false;

                // Hide highest rank (kingdom)
                rank_dropdown[rank_dropdown.length-2].hidden = true
                // Hide All option rank
                rank_dropdown[rank_dropdown.length-1].hidden = true
                // If highest rank selected, select second-highest rank (phylum)
                if (rank_dropdown.value === all_rank[all_rank.length-1] ||
                        rank_dropdown.value === 'all') {
                    rank_dropdown.value = all_rank[all_rank.length-2]
                }

                set_higher(rank_dropdown, higher_rank_dropdown, all_rank)
            } else if (radiobutton.value === 'global') {
                higher_rank_dropdown.disabled = true;

                // Show Kingdom rank
                rank_dropdown[rank_dropdown.length-2].hidden = false
                // Show All option rank
                rank_dropdown[rank_dropdown.length-1].hidden = false

                higher_rank_dropdown.value = 'all';
            }
        })
    }

    // Hide higher rank option that are the same or lower than the selected rank
    rank_dropdown.addEventListener('change', function() {
        if (!higher_rank_dropdown.disabled) {

            let index = set_higher(rank_dropdown, higher_rank_dropdown, all_rank)

            for (let i = 0; i < index; i++) {
                higher_rank_dropdown[i].hidden = true
            }
            for (let i = index; i < all_rank.length; i++) {
                higher_rank_dropdown[i].hidden = false
            }
        }
    })
})

// Sets higher_rank to one higher than selected at rank
// Returns index of selected rank in all_rank array
function set_higher(rank_dropdown, higher_rank_dropdown, all_rank) {
    let selected_rank = rank_dropdown.value

    let index = all_rank.findIndex(object => {
        return object === selected_rank
    })

    if (index === all_rank.length-1) {
        higher_rank_dropdown.value = all_rank[index]
    } else {
        higher_rank_dropdown.value = all_rank[index + 1]
    }

    return index
}
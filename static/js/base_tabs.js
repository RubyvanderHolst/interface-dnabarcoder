function switch_home_settings(button) {
    // Switches between "Home" and "Settings" tab
    if (button.id === "home_button") {
        if (check_settings()){
            button.classList.add("active");
            document.getElementById("settings_button").classList.remove("active");

            document.getElementById("div_home").classList.remove('hidden');
            document.getElementById("div_settings").classList.add('hidden');
            document.getElementById("div_explanation").classList.remove('hidden');
        } else {
            document.getElementById('id_form').reportValidity()
        }
    } else if (button.id === "settings_button") {
        button.classList.add("active");
        document.getElementById("home_button").classList.remove("active");

        document.getElementById("div_home").classList.add('hidden');
        document.getElementById("div_settings").classList.remove('hidden');
        document.getElementById("div_explanation").classList.add('hidden');
    }
}

function check_settings(){
    // Checks if settings have correct input
    let number_inputs = document.querySelectorAll('#div_settings input')
    for (let i = 0; i < number_inputs.length; i++) {
        let correct = number_inputs[i].checkValidity()
        if (!correct) {
            return false
        }
    }
    return true
}
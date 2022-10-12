function switch_home_settings(button) {
    if (button.id === "home_button") {
        if (check_settings()){
            button.classList.add("active");
            document.getElementById("settings_button").classList.remove("active");

            document.getElementById("div_home").style.display = "block";
            document.getElementById("div_settings").style.display = "none";
        }
    } else if (button.id === "settings_button") {
        document.getElementById("home_button").classList.remove("active");
        button.classList.add("active");

        document.getElementById("div_home").style.display = "none";
        document.getElementById("div_settings").style.display = "block";
    }
}

// Checks if settings have correct input
function check_settings(){
    let number_inputs = document.querySelectorAll('#div_settings input')
    for (let i = 0; i < number_inputs.length; i++) {
        let correct = number_inputs[i].checkValidity()
        if (!correct) {
            return false
        }
    }
    return true
}
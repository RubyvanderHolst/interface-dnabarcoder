function switch_home_settings(button) {
    if (button.id === "home_button") {
        button.classList.add("active");
        document.getElementById("settings_button").classList.remove("active");

        document.getElementById("div_home").style.display = "block";
        document.getElementById("div_settings").style.display = "none";
    } else if (button.id === "settings_button") {
        document.getElementById("home_button").classList.remove("active");
        button.classList.add("active");

        document.getElementById("div_home").style.display = "none";
        document.getElementById("div_settings").style.display = "block";
    }
}
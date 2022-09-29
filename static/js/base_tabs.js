function switch_home_settings(button) {
    if (button.id === "home_button") {
        button.classList.add("active");
        document.getElementById("settings_button").classList.remove("active");

        console.log("home", button.classList)
        console.log("settings", document.getElementById("settings_button").classList)

        document.getElementById("div_home").style.display = "block";
        document.getElementById("div_settings").style.display = "none";
    } else if (button.id === "settings_button") {
        document.getElementById("home_button").classList.remove("active");
        button.classList.add("active");

        console.log("settings", button.classList)
        console.log("home", document.getElementById("settings_button").classList)

        document.getElementById("div_home").style.display = "none";
        document.getElementById("div_settings").style.display = "block";
    }
}
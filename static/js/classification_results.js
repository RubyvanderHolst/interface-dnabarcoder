import {get_data} from "./base_results.js";

document.addEventListener("DOMContentLoaded", function(){
    let task_id = document.getElementById('task_id').innerText
    get_data(task_id, 'results/' + task_id, false, false)
})

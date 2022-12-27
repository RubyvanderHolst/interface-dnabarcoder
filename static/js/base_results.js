export {get_data}

// This function contains an AJAX function. It calls a URL which equals
// the task ID. This URL is connected to the view "load_progress", which
// returns a JsonResponse. This JsonResponse is processed by the AJAX function.
function get_data(task_id, media_dir, bool_show_image,
                  bool_show_classification, loading_time = 0) {
    $.ajax({
        url: "results/" + task_id,
        type: "GET",
        dataType: "json",
        // Response generated without error
        success: (data) => {
            document.getElementById('task_status').innerHTML = data.state.toLowerCase();
            // Task has successfully finished
            if (data.state === 'SUCCESS'){
                document.getElementById('spinner-box').classList.add('hidden');
                document.getElementById('data-box').classList.remove('hidden');

                // Show alert if no results were generated
                if (!data.has_results) {
                    document.getElementById('div_alert').innerHTML =
                        `<div class="alert alert-danger" role="alert">
                            No results could be generated! Please look at the input and settings.
                        </div>`
                }

                // Show html for table files
                if (data.files !== null) {
                    show_file_table(data.files)
                }

                // Create and show html for images
                if (bool_show_image) {
                    show_images(data.images, media_dir)
                }

                // Show classified sequences table
                if (bool_show_classification && data.classification_table !== null) {
                    show_classification(data.classification_table, data.table_file_path)
                }

            // Task is still being processed
            } else if (data.state === 'PENDING') {
                let reload_time = 1
                let reload_text = 'millisecond'
                if (loading_time < 10 * 10**3) {
                    reload_time = 10**3
                    reload_text = 'second'
                } else if (loading_time < 60 * 10**3) {
                    reload_time = 10 * 10**3
                    reload_text = '10 seconds'
                } else if (loading_time < 5*60 * 10**3) {
                    reload_time = 60 * 10**3
                    reload_text = 'minute'
                } else {
                    reload_time = 5 * 60 * 10**3
                    reload_text = '5 minutes'
                }

                // Recall get_data (current AJAX function) after delay
                document.getElementById('reload_time').innerText = reload_text
                setTimeout(function(){
                    get_data(task_id, media_dir, bool_show_image, bool_show_classification, loading_time += reload_time);
                    }, reload_time)

            } else if (data.state === 'FAILURE') {
                document.getElementById('spinner-box').classList.add('hidden');
                document.getElementById('data-box').classList.remove('hidden');
                document.getElementById('div_alert').innerHTML =
                        `<div class="alert alert-danger" role="alert">
                            The task resulted in a failure. Please look at your input.
                        </div>`
            }
        },
        // Response generated with error
        error: (error) => {
            console.error('error', error)

            document.getElementById('spinner-box').classList.add('hidden');
            document.getElementById('data-box').classList.remove('hidden');

            document.getElementById('div_alert').innerHTML =
                 `<div class="alert alert-danger" role="alert">
                    An error has occurred!
                 </div>`
        }
    })
}

function show_file_table (files) {
    // Creates a table of results files
    // parameters:
    // - files: Object with format {file_name: file_size}
    // - media_dir: Directory in media directory where results are stored
    document.getElementById('data-box').innerHTML +=
        `
        <h4 class="rounded-2 text-center light-blue-background">Result files</h4>
        `
    document.getElementById('data-box').innerHTML += files
}

function show_images(images, media_dir) {
    // Create cards with all images in results files
    // parameters:
    // - images: Object with format {file_name: file_size}
    // - media_dir: Directory in media directory where results are stored
    let list_images = Object.entries(images)
    if (list_images.length > 0){
        document.getElementById('images_div').innerHTML =
            `<h4 class="rounded-2 text-center light-blue-background">Images</h4>`
    }

    for (const [image_name, image_size] of list_images) {
        let image_card =
            `
            <div class="card mx-auto w-50 bg-light border-dark">
                <h5 class="card-header text-center">${image_name} (${image_size})</h5>
                <div class="card-body text-center">
                    <div class="row">
                        <img src="/media/${media_dir}/${image_name}" class="border">
                    </div>
                    <div class="row">
                        <a href="/media/${media_dir}/${image_name}" class="link-light text-decoration-none" download>
                            <button type='button' class='btn btn-primary'><i class="bi bi-download"></i> Download</button>
                        </a>
                    </div>
                </div>
            </div>
            `
        document.getElementById('images_div').innerHTML += image_card
    }
}


function show_classification(table, file_path) {
    document.getElementById('classification_results_table').innerHTML +=
        `
        <h4 class="rounded-2 text-center light-blue-background">Classified sequences</h4>
        <a href='${file_path}' class='link-light text-decoration-none'>
            <button type='button' class='btn btn-light w-100 mb-10'><i class='bi bi-download'></i> Download table</button>
        </a>
        `
    document.getElementById('classification_results_table').innerHTML +=
        table
}

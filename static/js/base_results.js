export {get_data}

function get_data(task_id, media_dir, bool_show_image, bool_show_complex, loading_time = 0) {
          $.ajax({
               url: task_id,
               type: "GET",
               dataType: "json",
               success: (data) => {
                    document.getElementById('task_status').innerHTML = data.state
                    if (data.state === 'SUCCESS'){
                        document.getElementById('spinner-box').classList.add('hidden');
                        document.getElementById('data-box').classList.remove('hidden');

                        // Show alert if no results were generated
                        if (!data.has_results) {
                            document.getElementById('div_alert').innerHTML =
                                    `<div class="alert alert-danger" role="alert">
                                        No results could be generated, please change the settings!
                                    </div>`
                        }
                        // Create html for table files
                        if (Object.entries(data.files).length !== 0 ) {
                            show_file_table(data.files, media_dir)
                        }
                        // Create html for images
                        if (bool_show_image) {
                            show_images(data.images, media_dir)
                        }
                        // Create html for same complexes
                        if (bool_show_complex && data.similar) {
                            show_similar_seq(data.similar)
                        }
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

                        document.getElementById('reload_time').innerText = reload_text
                        setTimeout(function(){
                            get_data(task_id, media_dir, bool_show_image, bool_show_complex, loading_time += reload_time);
                        }, reload_time)
                    }
               },
               error: (error) => {
                    console.error('error', error)

                    document.getElementById('spinner-box').classList.add('hidden');
                    document.getElementById('data-box').classList.remove('hidden');

                    document.getElementById('data-box').innerHTML =
                        `
                        <div class="alert alert-danger" role="alert">
                            An error has occurred!
                        </div>
                        `
               }
          })
}

function show_file_table (files, media_dir) {
    document.getElementById('data-box').innerHTML +=
        `
        <table class="table table-bordered">
            <thead>
                <tr class="table-success">
                    <th scope="col">File name</th>
                    <th scope="col">File size</th>
                    <th scope="col"></th>
                </tr>
            </thead>
            <tbody id="tbody_files">
            </tbody>
        </table>
        `
    for (const [file_name, file_size] of Object.entries(files)) {
        console.log(file_name)
        let tr = "<tr>";
        tr +=
            `
            <td>${file_name}</td>
            <td>${file_size}</td>
            <td>
                <a href='/media/${media_dir}/${file_name}' class='link-light text-decoration-none' download="${file_name}">
                    <button type='button' class='btn btn-success w-100'>Download</button>
                </a>
            </td></tr>`
            document.getElementById('tbody_files').innerHTML += tr;
    }
}

function show_images(images, media_dir) {
    let list_images = Object.entries(images)
    for (const [image_name, image_size] of list_images) {
        let image_card =
            `
            <div class="card mx-auto w-50">
                <h5 class="card-header text-center">${image_name} (${image_size})</h5>
                <div class="card-body text-center">
                    <img src="/media/${media_dir}/${image_name}" class="img-fluid">
                     <a href="/media/${media_dir}/${image_name}" class="link-light text-decoration-none" download>
                        <button type="button" class="btn btn-success">Download</button>
                     </a>
                </div>
            </div>
            `
        document.getElementById('images_div').innerHTML += image_card
    }
}

function show_similar_seq(similar) {
    document.getElementById('complexes_div').innerHTML = `<h4>Removed similar sequences</h4>`
    let list_complexes =  Object.entries(similar)
    if (list_complexes.length === 0) {
        document.getElementById('complexes_div').innerHTML +=
            `
            <div class="alert alert-secondary" role="alert">
                No similar sequences were found
            </div>
            `
    }

    for (const [cluster, obj_ids] of list_complexes) {
        let html_table =
            `
            <table class="table table-bordered">
                <thead>
                    <tr><th class="text-center table-dark" colspan="2">Cluster ${cluster}</th></tr>
                    <tr>
                        <th class="table-success w-50p" scope="col">Preserved sequences</th>
                        <th class="table-danger w-50p" scope="col">Removed sequences</th>
                    </tr>
                </thead>
                <tbody>
            `

        const array_representing = obj_ids['representing']
        const array_removed = obj_ids['removed']
        const max_len = Math.max(array_representing.length, array_removed.length)
        for (let row=0; row<max_len; row++) {
            html_table += `<tr>`
            if (row < array_representing.length) {
                html_table += `<td>${array_representing[row]}</td>`
            } else {
                html_table += `<td></td>`
            }

            if (row < array_removed.length) {
                html_table += `<td>${array_removed[row]}</td>`
            } else {
                html_table += '<td></td>'
            }

            html_table += `</tr>`
        }
        html_table += '</tbody></table>'
        document.getElementById('complexes_div').innerHTML += html_table;
    }
}

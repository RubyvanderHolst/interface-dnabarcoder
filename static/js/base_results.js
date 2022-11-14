export {get_data}

function get_data(task_id, media_dir, bool_show_image) {
          $.ajax({
               url: task_id,
               type: "GET",
               dataType: "json",
               success: (data) => {
                    document.getElementById('task_status').innerHTML = data.state
                    if (data.state === 'SUCCESS'){
                        document.getElementById('spinner-box').classList.add('hidden');
                        document.getElementById('data-box').classList.remove('hidden');

                         // Create html for table files
                         for (const [file_name, file_size] of Object.entries(data.files)) {
                              let tr = "<tr>";
                              tr += `<td>
                                        ${file_name}
                                     </td>
                                     <td>
                                        ${file_size}
                                     </td>
                                     <td>
                                        <button type='button' class='btn btn-success w-100'>
                                            <a href='/media/${media_dir}/${file_name}' class='link-light text-decoration-none' download="${file_name}">
                                                Download
                                            </a>
                                        </button>
                                     </td></tr>`
                             document.getElementById('tbody-base').innerHTML += tr;
                         }

                        // Create html for images
                        if (bool_show_image) {
                            let list_images = Object.entries(data.images)
                            if (list_images.length === 0){
                                document.getElementById('images_div').innerHTML =
                                    `<div class="alert alert-danger" role="alert">
                                        No results could be generated, please change the settings!
                                    </div>`
                            } else {
                                for (const [image_name, image_size] of list_images) {
                                    let image_card =
                                        `<div class="card mx-auto w-50">
                                            <h5 class="card-header text-center">${image_name} (${image_size})</h5>
                                            <div class="card-body text-center">
                                                <img src="/media/${media_dir}/${image_name}" class="img-fluid">
                                                <button type="button"
                                                        class="btn btn-success">
                                                    <a href="/media/${media_dir}/${image_name}"
                                                       class="link-light text-decoration-none"
                                                       download>
                                                        Download
                                                    </a>
                                                </button>
                                            </div>
                                        </div>`
                                    document.getElementById('images_div').innerHTML += image_card
                                }
                            }
                        }

                    } else {
                         setTimeout(function(){
                              get_data(task_id, media_dir, bool_show_image);
                              }, 1000) // Wait 1 second until reload
                    }
                    },
               error: (error) => {
                    document.getElementById('task_status').innerHTML = 'ERROR'
                    console.log('error', error)
                    document.getElementById('data-box').innerHTML = 'An error has occurred'
                    setTimeout(function(){
                         get_data(task_id, media_dir, bool_show_image);
                         }, 1000) // Wait 1 seconds
                    }
               })
     }
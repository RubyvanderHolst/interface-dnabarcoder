document.addEventListener('DOMContentLoaded', function () {
     let task_id = document.getElementById('task_id').innerText

     get_data()

     function get_data() {
          $.ajax({
               url: task_id,
               type: "GET",
               dataType: "json",
               success: (data) => {
                    document.getElementById('task_status').innerHTML = data.state
                    if (data.state === 'SUCCESS'){
                        document.getElementById('spinner-box').style.display = "none";
                         document.getElementById('data-box').style.display = "block";

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
                                            <a href='/media/cutoff/${file_name}' class='link-light text-decoration-none' download="${file_name}">
                                                Download
                                            </a>
                                        </button>
                                     </td></tr>`
                             document.getElementById('tbody-base').innerHTML += tr;
                         }

                        for (const [image_name, image_size] of Object.entries(data.images)) {
                            let image_card =
                                `<div class="card mx-auto w-50">
                                    <h5 class="card-header text-center">${image_name} (${image_size})</h5>
                                    <div class="card-body text-center">
                                        <img
                                            src="/media/cutoff/${image_name}"
                                            class="img-fluid">
                                            <button type="button"
                                                    class="btn btn-success">
                                                <a href="/media/cutoff/${image_name}"
                                                   class="link-light text-decoration-none"
                                                   download>
                                                    Download
                                                </a>
                                            </button>
                                    </div>
                                </div>`
                            document.getElementById('images_div').innerHTML += image_card
                        }

                    } else {
                         setTimeout(function(){
                              get_data();
                              }, 1000) // Wait 1 second until reload
                    }
                    },
               error: (error) => {
                    console.log('error', error)
                    document.getElementById('data-box').innerHTML = 'An error has occurred'
                    setTimeout(function(){
                         get_data();
                         }, 1000) // Wait 1 seconds
                    }
               })
     }
})
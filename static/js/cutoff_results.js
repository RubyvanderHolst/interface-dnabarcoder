document.addEventListener('load', function() {
    document.getElementById('loading').style.display = "none";
    document.getElementById('done').style.display = "block";
})

// learn to use ajax to get data afterwards
// https://stackoverflow.com/questions/59510573/how-can-i-show-a-loading-animation-in-django-while-the-server-is-processing-a-vi
// https://www.geeksforgeeks.org/handling-ajax-request-in-django/
// Using jQuery will make it significantly easier
// https://stackoverflow.com/questions/8567114/how-can-i-make-an-ajax-call-without-jquery
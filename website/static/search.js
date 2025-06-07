let starred = []

// Create a function that will show starred courses that I can call w/ Content Loaded & search bar

document.addEventListener("DOMContentLoaded", function(){
    fetch('/fetch-starred')
        .then(response => response.json())
        .then(results => {
            starred = results;
            displayStarred(); // CHANGE THIS ACCORDINGLY
            linkModal();
    });
});

document.getElementById('searchBar').addEventListener('input', function(event){
    let q = event.target.value;
    let showResults = document.getElementById('showResults');
    if (q == "") {
        displayStarred(); // CHANGE THIS ACCORDINGLY
    } else {
        // CHANGE THIS CODE
        for (course in starred) {
            showResults.innerHTML = "TEST"
        }
    }
    linkModal();
});

// Similar code to course.js - Figure out how to reduce redundant code
function linkModal() {
    document.querySelectorAll('.course-title').forEach(title => {
        title.addEventListener('mouseover', function(){
        title.style.color = "#fcba03";
        title.style.textDecoration = "underline";
        });
        title.addEventListener('mouseout', function(){
            title.style.color = "";
            title.style.textDecoration = "";
        });
        title.addEventListener('click', function(){
            // CHANGE ALL THIS SHITE
            let id = title.getAttribute('data-course-id');
            let course_modal = new bootstrap.Modal(document.getElementById('course_' + id));
            course_modal.show();
        });
    });
}

// Should make this into two functions - (1) Display all courses in starred (2) Find all starred elements and add icon
function displayStarred() {
    let showResults = document.getElementById('showResults');
    let html = "";
    for (const course of starred) {
        html += `<li class="list-group-item"> <h5 class="course-title"> ${course.title} </h5> <p style="color: #787878"> ${course.desc} </p>
                    <div class="d-flex justify-content-end">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="22"
                            height="22"
                            class="bi bi-star-fill"
                            viewBox="0 0 16 16"
                            style="fill: #ffca1d"
                        >
                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                        </svg>
                    </div>
                </li>`;
    }
    showResults.innerHTML = html;
}
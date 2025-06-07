let starred = []
let starred_id = []
let qresults = []
let cart = [] // [{id, title} ...]

document.addEventListener("DOMContentLoaded", function(){
    fetch('/fetch-starred')
        .then(response => response.json())
        .then(results => {
            starred = results;
            for (const course of starred) { starred_id.push(course.id) }
            displayResults(starred);
            addStarIcon();
            linkModal();
    });
});

document.getElementById('searchBar').addEventListener('input', function(event){
    let q = event.target.value;
    let showResults = document.getElementById('showResults');
    if (q == "") {
        displayResults(starred);
        addStarIcon();
    } else if (q.length >= 3) {
        fetch('/search-keyword', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q })
    }).then(response => response.json())
      .then(results => {
        qresults = results;
        displayResults(qresults);
        addStarIcon();
        linkModal();
        });
    }
    linkModal();
});

// View Cart
document.getElementById('viewCart').addEventListener('click', function(){
    let body = document.getElementById('viewCartModalBody');
    if (!cart.length) {
        body.innerHTML = `<h5 class="m-2" style="color: #b4b4b4; text-align: center"> <em> No courses added to cart! </em> </h5>
                            <p style="color: #b4b4b4; text-align: center"> To add a course, click its title on the search menu and select 'Add to Cart'. </p>`;
    } else {
        let html = `<ul class = "list-group">`;
        for (const dict of cart) {
            html += `<li class="list-group-item"> <strong> ${dict.title} </strong> </li>`;
        }
        html += `</ul>`;
        body.innerHTML = html;
    }
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

// list is a list of dicts with keys id, title, desc
function displayResults(list) {
    let showResults = document.getElementById('showResults');
    let html = "";
    for (const course of list) {
        if (starred_id.includes(course.id)) {
            html += `<li class="list-group-item"> 
                        <div class="starred"> 
                            <h5 class="course-title"> ${course.title} </h5> <p style="color: #787878"> ${course.desc} </p>
                            <div class="d-flex justify-content-end"> <div class="if-starred"> </div> </div> 
                        </div>
                    </li>`;
        } else {
            html += `<li class="list-group-item"> 
                        <h5 class="course-title"> ${course.title} </h5> <p style="color: #787878"> ${course.desc} </p>
                    </li>`;
        }
    }
    showResults.innerHTML = html;
}

function addStarIcon() {
    document.querySelectorAll('.starred').forEach(course => {
        icon = course.querySelector('.if-starred');
        icon.innerHTML = `<svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="22"
                            height="22"
                            class="bi bi-star-fill"
                            viewBox="0 0 16 16"
                            style="fill: #ffca1d"
                        > <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                        </svg>`;
    });
}

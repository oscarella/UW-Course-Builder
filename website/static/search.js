let starred = []
let starred_id = []
let qresults = []
let cart = [] // [{id, title} ...]

/*
    When page loads, reset user's starred courses
    starred_id contains only course ids for easy comparison
*/
document.addEventListener("DOMContentLoaded", function(){
    fetch('/fetch-starred')
    .then(response => response.json())
    .then(results => {
        starred = results;
        starred_id = []
        for (const course of starred) { 
            starred_id.push(course.id) 
        }
        let searchBar = document.getElementById('searchBar');
        searchBar.value = "";
        searchBar.dispatchEvent(new Event('input', { bubbles: true }));
    });
});

// Listener performs live search for user course queries
document.getElementById('searchBar').addEventListener('input', function(event){
    let q = event.target.value;
    let showResults = document.getElementById('showResults');
    if (q == "") {
        displayResults(starred);
    } else if (q.length >= 3) { // Server returns query response via whooshee_search()
        fetch('/search-keyword', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q })
    }).then(response => response.json())
      .then(results => {
        qresults = results;
        displayResults(qresults);
        });
    }
});

// View courses selected by user for "checkout"
document.getElementById('viewCart').addEventListener('click', function(){
    let body = document.getElementById('viewCartModalBody');
    if (!cart.length) {
        body.innerHTML = `<h5 class="m-2" style="color: #b4b4b4; text-align: center"> <em> No courses added to cart! </em> </h5>
                            <p style="color: #b4b4b4; text-align: center"> To add a course, click its title on the search menu and select 'Add to Cart'. </p>`;
    } else {
        let html = `<p class="d-flex justify-content-center" style="color: red"> <strong> Warning: Your cart is emptied when you refresh the page! </strong> </p> <ul class = "list-group">`;
        for (const dict of cart) {
            html += `<li class="list-group-item"> <strong> ${dict.title} </strong> </li>`;
        }
        html += `</ul>`;
        body.innerHTML = html;
    }
});

// list is a list of dicts with keys: id, title, desc, body
function displayResults(list) {
    let showResults = document.getElementById('showResults');
    let html = "";
    for (const course of list) {
        /*
        data-course-id, data-bs-toggle, data-bs-target: Used by modal to determine which course description to display
        Star button (data-item-id, class[starred, 'not starred']) Used for modifyStarredStatus
        */
        // OTHERWISE WHITE BUT BORDER WHITE ; BUTTON has white background
        if (starred_id.includes(course.id)) {
            html += `<li class="list-group-item"> 
                        <h5 class="course-title" data-course-id="${course.id}"
                        data-bs-toggle="modal" data-bs-target="#courseViewerModal"> ${course.title} </h5> <p style="color: #787878"> ${course.desc} </p>
                        <div class="d-flex justify-content-end"> 
                            <button
                                type="button"
                                class="btn star"
                                data-item-id="${course.id}"
                                style="background-color: white"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    class="bi bi-star-fill starred"
                                    fill="#ffca1d"
                                    stroke="black"
                                    stroke-width="1.5"
                                    viewBox="0 0 16 16"
                                >
                                    <path
                                    d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
                                    />
                                </svg>
                            </button>
                        </div> 
                    </li>`;
        } else {
            html += `<li class="list-group-item"> 
                        <h5 class="course-title" data-course-id="${course.id}" data-bs-toggle="modal" data-bs-target="#courseViewerModal"> 
                        ${course.title} </h5> <p style="color: #787878"> ${course.desc} </p>
                        <div class="d-flex justify-content-end"> 
                            <button
                                type="button"
                                class="btn star"
                                data-item-id="${course.id}"
                                style="background-color: white"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    class="bi bi-star-fill notstarred"
                                    fill="white"
                                    stroke="black"
                                    stroke-width="1.5"
                                    viewBox="0 0 16 16"
                                >
                                    <path
                                    d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
                                    />
                                </svg>
                            </button>
                        </div> 
                    </li>`;
        }
    }
    showResults.innerHTML = html;
    modifyStarredStatus();
    linkModal();
}

// Adds listeners to modify starred status via star icon
// C+Ped code from starred.js (Reduce redundancy here)
function modifyStarredStatus() {
    document.querySelectorAll('.btn.star').forEach(starbtn => {
        starbtn.addEventListener('mouseover', function(){
            let icon = starbtn.querySelector('svg');
            if (icon.classList.contains('starred')) {
                icon.style.fill = 'white'
            } else if (icon.classList.contains('notstarred')) {
                icon.style.fill = '#ffca1d'
            }
        });
        starbtn.addEventListener('mouseout', function(){
            let icon = starbtn.querySelector('svg');
            icon.style.fill = '';
        });
        starbtn.addEventListener('click', function() {
            let id = starbtn.getAttribute('data-item-id');
            // Modifies starred element, updates starred & refreshes search bar
            fetch('/star-course-search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ courseId: id })
            }).then(results => results.json())
              .then((courses) => {

                starred = courses;
                starred_id = []
                for (const course of starred) { 
                    starred_id.push(course.id) 
                }
                let searchBar = document.getElementById('searchBar');
                searchBar.value = "";
                searchBar.dispatchEvent(new Event('input', { bubbles: true }));
            });
        });
    });
}

// Links title with modal
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
            // Populates text and buttons of modal
            let courseId = title.getAttribute('data-course-id');
            fetch('/search-course-id', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ courseId: courseId })
            }).then(response => response.json())
              .then(course => {
                let modal = document.getElementById('courseViewerModal');
                modal.querySelector('.modal-title').innerHTML = course.title; // Header
                // Prettifies course desecription (Adds HTML tags and bullet pints)
                fetch('/prettify-desc', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ courseBody: course.body })
                }).then(response => response.json())
                  .then(newBody => {
                    modal.querySelector('.modal-body-text').innerHTML = course.desc + `</br> </br>` + newBody; // Body
                });
                let footer = modal.querySelector('.modal-footer'); // Footer
                let cartId = []
                for (const c of cart) { cartId.push(c.id) }
                if (cartId.includes(course.id)) {
                    footer.innerHTML = 
                        `<div class="d-flex">
                            <button type="button" class="btn btn-primary btn-lg" disabled>
                                Course Already in Cart
                            </button>
                        </div>`
                    addToCart(course.id, course.title);
                } else {
                    fetch('/check-status', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ courseId: course.id })
                    }).then(response => response.json())
                      .then(result => {
                        if (result) { // Course already in schedule
                            footer.innerHTML = 
                                `<div class="d-flex">
                                    <button type="button" class="btn btn-primary btn-lg" disabled>
                                        Course Already in Schedule
                                    </button>
                                </div>`
                        } else {
                            footer.innerHTML = 
                                `<div class="d-flex">
                                    <button type="button" class="btn btn-primary btn-lg" id="addCourseToCart">
                                        Add to Cart
                                    </button>
                                </div>`
                        }
                        addToCart(course.id, course.title);
                    });
                }
            });
        }); 
    });
}

// Adds course to cart if button selected
function addToCart(id, title) {
    let b = document.getElementById('addCourseToCart');
    let B = b.cloneNode(true)
    b.parentNode.replaceChild(B, b)

    B.addEventListener('click', function() {
        cart.push({id: id, title: title});
        let modalElement = document.getElementById('courseViewerModal');
        let modal = bootstrap.Modal.getOrCreateInstance(modalElement);
        modal.hide();
    });
}

// Sends POST request to backend when user finalizes 'Checkout'
let checkoutBtn = document.getElementById('finishCheckout');
checkoutBtn.addEventListener('click', function() {
    let termSelected = document.getElementById('termOptions').value;
    fetch('/add-courses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ courses: cart, term: termSelected })
    }).then((_res) => {
        window.location.href = "/";
    });
})

// Listener for when user selects 'Checkout'
let checkout = document.getElementById('checkoutTerm');
checkout.addEventListener('click', function() {
    fetch('/fetch-terms')
    .then(response => response.json())
    .then(result => {
        let terms = result; // [{term.id, term.name}]
        if (!terms.length) {
            let modalBody = document.getElementById('checkoutTermOptions');
            modalBody.innerHTML = `<h5 style="text-align: center"> You cannot add course(s) with no terms. 
                                    To create a term, go to 'Home'. </h5>`;
        } else {
            let html = "";
            for (const term of terms) {
                html += `<option value="${term.id}"> ${term.name} </option>`;
            }
            let list = document.getElementById('termOption');
            list.innerHTML = html;
        }
    });
})

// Listener to ensure user selects proper term during 'Checkout'
let options = document.getElementById('termOptions');
options.addEventListener('change', function() {
    let checkoutBtn = document.getElementById('finishCheckout');
    if (options.value != "-1") {
        checkoutBtn.disabled = false;
    } else {
        checkoutBtn.disabled = true;
    }
});
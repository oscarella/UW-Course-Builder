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
        let id = title.getAttribute('data-course-id');
        let course_modal = new bootstrap.Modal(document.getElementById('course_' + id));
        course_modal.show();
    });
});
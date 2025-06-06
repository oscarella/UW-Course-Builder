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
        var name = title.innerHTML;
        var course_modal = new bootstrap.Modal(document.getElementById('course_'+name));
        course_modal.show();
    });
});
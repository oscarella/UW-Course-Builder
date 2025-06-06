document.querySelectorAll('.btn.star').forEach(starbtn => {
  starbtn.addEventListener('mouseover', function(){
    var icon = starbtn.querySelector('svg');
    if (icon.classList.contains('starred')) {
      icon.style.fill = '#FFFFFF'
    } else if (icon.classList.contains('notstarred')) {
      icon.style.fill = '#ffca1d'
    }
  });
  starbtn.addEventListener('mouseout', function(){
    var icon = starbtn.querySelector('svg');
    icon.style.fill = '';
  });
  // Remove / Add to starred courses
  starbtn.addEventListener('click', function() {
    var id = starbtn.getAttribute('data-item-id');
    fetch('/star-course', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ courseId: id })
    }).then((_res) => {
      window.location.href = "/";
    });
  });
});
document.querySelectorAll('.btn.star').forEach(starbtn => {
  starbtn.addEventListener('mouseover', function(){
    icon = starbtn.querySelector('svg');
    if (icon.classList.contains('starred')) {
      icon.style.fill = '#FFFFFF'
    } else if (icon.classList.contains('notstarred')) {
      icon.style.fill = '#ffca1d'
    }
  });
  starbtn.addEventListener('mouseout', function(){
    icon = starbtn.querySelector('svg');
    icon.style.fill = '';
  });
});
$(function() {
  function handleDragStart(e) {
    this.style.opacity = '0.4';
  
    dragSrcEl = this;
  
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
  }
  
  function handleDragEnd(e) {
    e.stopPropagation();
  
    if (dragSrcEl !== this) {
      dragSrcEl.innerHTML = this.innerHTML;
      this.innerHTML = e.dataTransfer.getData('text/html');
    }
  
    return false;
  }

  let items = document.querySelectorAll('.pl-dataframe-complete-piece');
  items.forEach(function (item) {
    item.addEventListener('dragstart', handleDragStart);
    item.addEventListener('dragend', handleDragEnd);
  });
})

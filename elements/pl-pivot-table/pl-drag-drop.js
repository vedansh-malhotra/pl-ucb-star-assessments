const allowDrop = event => {
    event.preventDefault();
};

const drag = event => {
    event.dataTransfer.setData('text/html', event.currentTarget.outerHTML);
    event.dataTransfer.setData('text/plain', event.currentTarget.dataset.id);
};

const dragEnd = target => {
    target.classList.remove('dragging');
};

function dragStart(target) {
    target.classList.add('dragging');
};

document.querySelectorAll('.col-set').forEach(colset => {
    console.log(colset);
    colset.addEventListener('dragstart', dragStart);
    colset.addEventListener('dragend', dragEnd);
});
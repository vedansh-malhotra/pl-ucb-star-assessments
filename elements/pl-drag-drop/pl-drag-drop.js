$(function() {
    $(".dataframe tbody tr").draggable({
        helper: "clone",
        opacity: 0.5,
        zIndex: 1000
    });

    $(".dataframe th").draggable({
        helper: "clone",
        opacity: 0.5,
        zIndex: 1000
    });

    $(".dataframe tbody tr, .dataframe th").droppable({
        accept: ".dataframe tbody tr, .dataframe th",
        drop: function(event, ui) {
            var draggable = ui.draggable;
            var droppable = $(this);

            // Swap the content of the dragged and dropped cells
            var temp = droppable.html();
            droppable.html(draggable.html());
            draggable.html(temp);

            const thElements = document.querySelectorAll('th');
            const tdElements = document.querySelectorAll('td');
            
            var x = document.getElementsByClassName("dataframe");
            var id_answer_name = '#' + answer_name + '-input';
            $(id_answer_name).val(x[0].outerHTML);
        }
    });
    
})

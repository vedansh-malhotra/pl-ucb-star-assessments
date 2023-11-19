$(function() {
    //Change selection method in future to specify the current question(uuid)
    var row = Array.from({length: num_row}, x => null);
    var answer = {'column':null,'index':null,'rows':row};

    $(".col-set").draggable({
        helper: "clone",
        zIndex: 100,
        start: function (event, ui) {
            var w = $(this).css('width');
            var h = $(this).css('height');
            $(this).css({
                opacity: 0.5
            });
            ui.helper.css('width', w).css('height', h);
          },
        stop: function (event, ui) {
            var w = $(this).css('width');
            var h = $(this).css('height');
            $(this).css({
                opacity: 1
            });
            ui.helper.css('width', w).css('height', h);
          }
        
    });

    $(".index").draggable({
        helper: "clone",
        zIndex: 100,
        start: function (event, ui) {
            var w = $(this).css('width');
            var h = $(this).css('height');
            $(this).css({
                opacity: 0.5
            });
            ui.helper.css('width', w).css('height', h);
          },
        stop: function (event, ui) {
            var w = $(this).css('width');
            var h = $(this).css('height');
            $(this).css({
                opacity: 1
            });
            ui.helper.css('width', w).css('height', h);
          }
        
    });

    $(".drop-zone-col").droppable({
        accept: ".col-set",
        drop: function(event, ui) {
            var draggable = ui.draggable;
            var droppable = $(this);

            let drag_cols = Array.from(draggable.find('.col-md-2'));
            let drop_cols = Array.from(droppable.find('.col-md-2'));
            drag_cols.forEach(function(ele, index){
                drop_cols[index].textContent = ele.textContent;
                $(drop_cols[index]).addClass('dropped-color-col');
            })

            var col_num = $(ui.helper).attr('data-order');
            var id_answer_name = '#' + uuid + '-input';
            answer['column'] = col_num;
            $(id_answer_name).val(JSON.stringify(answer));

        }
    });

    $(".drop-zone-index").droppable({
        accept: ".index",
        drop: function(event, ui) {
            var draggable = ui.draggable;
            var droppable = $(this);

            let drag_cols = Array.from(draggable.find('.col-md-12'));
            let drop_cols = Array.from(droppable.find('.col-md-12'));
            drag_cols.forEach(function(ele, index){
                drop_cols[index].textContent = ele.textContent;
                $(drop_cols[index]).addClass('dropped-color-index');
            })
            
            var index_num = $(ui.helper).attr('data-order');
            var id_answer_name = '#' + uuid + '-input';
            answer['index'] = index_num;
            $(id_answer_name).val(JSON.stringify(answer));
        }
    });

    $(".drop-zone-row").droppable({
        accept: ".index",
        drop: function(event, ui) {
            var draggable = ui.draggable;
            var droppable = $(this);

            let drag_cols = Array.from(draggable.find('.col-md-12'));
            let drop_cols = Array.from(droppable.find('.col-md-12'));
            drag_cols.forEach(function(ele, index){
                drop_cols[index].textContent = ele.textContent;
                $(drop_cols[index]).addClass('dropped-color-row');
            })

            var row_num = $(ui.helper).attr('data-order');
            var id_answer_name = '#' + uuid + '-input';
            var dropzone_num = droppable.attr('order');
            dropzone_num = parseInt(dropzone_num);
            answer['rows'][dropzone_num] = row_num;
            $(id_answer_name).val(JSON.stringify(answer));

        }
    });

    //Change selector in future to specify button only for the current question
    $("#unique").click(function(){
        //Change selection method in future to specify the current question(uuid)
        let cols = document.querySelectorAll(".drop-col");
        let indice = document.querySelectorAll(".drop-index");
        let rows = document.querySelectorAll(".drop-row");
        cols.forEach(ele => {
            $(ele).removeClass('dropped-color-col');
            ele.textContent = "Column";
        })
    
        indice.forEach(ele => {
            $(ele).removeClass('dropped-color-index');
            ele.textContent = "Index";
        })
    
        rows.forEach(ele => {
            $(ele).removeClass('dropped-color-row');
            ele.textContent = "\u00A0";
        })

        let reset_row = Array.from({length: num_row}, x => null);
        answer = {'column':null,'index':null,'rows':reset_row};
        var id_answer_name = '#' + uuid + '-input';
        $(id_answer_name).val(JSON.stringify(answer));
    });

});
$(function() {
    $("#author_autocomplete").autocomplete({
        source: %s,
        focus: function(event, ui) {
            event.preventDefault();
            $(this).val(ui.item.label);
        },
        change: function(event, ui) {
            event.preventDefault();
            if (!ui.item){
                var fullname = this.value.split(', ');
                var first = fullname[1];
                var last = fullname[0];
                var add = confirm('Add '+first +' '+last+ ' to the DB?');
                if (add){
                    $("#first_name").val(first);
                    $("#last_name").val(last);
                };
            }
            else{
                event.preventDefault();
                $(this).val(ui.item.label);
                $("#author_ac_key").val(ui.item.value);
                $("#author_id").val(ui.item.value);
                $("#first_name").val(ui.item.first_name);
                $("#last_name").val(ui.item.last_name);
            };
        }
    });
});


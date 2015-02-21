$(function() {                                                  
    $("#series_autocomplete").autocomplete({
        source: %s,                                     
        focus: function(event, ui) {                    
            event.preventDefault();                  
            $(this).val(ui.item.label);              
        },                                        
        select: function(event, ui) {                   
            event.preventDefault();                 
            $(this).val(ui.item.label);             
            $("#series_ac_key").val(ui.item.value);
        }                                        
    });                                              
});                                                  

$(document).ready(function(){
    const csrftoken = $.cookie('csrftoken');
   
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $('.select2').select2({
        placeholder: 'Select an option',
        
      });
});
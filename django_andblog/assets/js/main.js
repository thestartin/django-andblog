(function (){
    //Main control function

    // Copy of the HTML of the main section, to be used later for adding multiple sections
    var mainSection = $('#sec_1').html();

    // Current section id to be used by del and add sections
    var sec_id = 1;

    var delSection = function(s_id){
        // This function deletes a give section
    };

    var resetSection = function(s_id){
        // This function resets values in a given section a give section
    };

    var funcs = {
        'del': delSection,
        'reset': resetSection
    };

    $('.sec_btn').on('click', function(){
        // Find the type of the button
        var btn = $(this).data('btnNm') ;
        var s_id = $(this).data('sectionId') ;
        if (btn == 'del' || btn == 'reset'){
            // Call the appropriate function
            funcs[btn](s_id);
        }
    });


})();
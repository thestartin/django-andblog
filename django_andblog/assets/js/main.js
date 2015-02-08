(function (){
    //Main control function

    // Copy of the HTML of the main section, to be used later for adding multiple sections
    var mainSection = $('<div class="section"></div>').append($('#sec').clone()).html();
    var mainHtml = $('<div class="section"></div>').append($(mainSection).remove('.norep')).html();

    // Current section id to be used by del and add sections
    var sec_id = 1;

    var delSection = function(s_id){
        // This function deletes a give section
    };

    var resetSection = function(s_id){
        // This function resets values in a given section a give section
    };

    var addSection = function(){
        // This function resets values in a given section a give section
        sec_id ++;
        var mainT = $(mainHtml);
        iId(mainT, true);
        $('form').append(mainT);
    };

    var iId = function (el, self){
        if (self){
            var o_id = el.attr('id');
            if (o_id) {
                var n_id = o_id + '_' + sec_id;
                el.attr('id', n_id);
            }
        }

        el.find('*').each(function (){
            var o_id = $(this).attr('id');
            if (o_id) {
                var n_id = o_id + '_' + sec_id;
                $(this).attr('id', n_id);
            }
        });
    };

    var funcs = {
        'del': delSection,
        'reset': resetSection,
        'add': addSection
    };

    $('.sec_btn').on('click', function(){
        // Find the type of the button
        var btn = $(this).data('btnNm') ;
        var s_id = $(this).data('sectionId') ;
        if (btn == 'del' || btn == 'reset' || btn == 'add'){
            // Call the appropriate function
            if (s_id){
                funcs[btn](s_id);
            } else {
                funcs[btn]();
            }
        }
    });


})();
(function (){
    //Main control function

    // Copy of the HTML of the main section, to be used later for adding multiple sections
    var mainSection = $('<div class="section"></div>').append($('#sec').clone()).html();
    mainSection = $(mainSection);
    $(mainSection).find('div.norep').remove();
    // You want mainHtml as string so object manipulations can be done later
    var mainHtml = $('<div id="sec" class="section"></div>').append(mainSection.clone()).html();

    // Current section id to be used by del and add sections
    var sec_id = 1;

    // TODO:
    // ckInit logic taken from django-ckeditor this needs to be replaced with calling init file
    var ckInit = function() {
      var djangoJQuery;
      if (typeof jQuery == 'undefined' && typeof django == 'undefined') {
        console.error('ERROR django-ckeditor missing jQuery. Set CKEDITOR_JQUERY_URL or provide jQuery in the template.');
      } else if (typeof django != 'undefined') {
        djangoJQuery = django.jQuery;
      }

      var $ = jQuery || djangoJQuery;
      $(function() {
        initialiseCKEditor();
        initialiseCKEditorInInlinedForms();

        function initialiseCKEditorInInlinedForms() {
          try {
            $(document).on("click", ".add-row a, .grp-add-handler", function () {
              initialiseCKEditor();
              return true;
            });
          } catch (e) {
            $(document).delegate(".add-row a, .grp-add-handler", "click",  function () {
              initialiseCKEditor();
              return true;
            });
          }
        }

        function initialiseCKEditor() {
          $('textarea[data-type=ckeditortype]').each(function(){
            if($(this).data('processed') == "0" && $(this).attr('id').indexOf('__prefix__') == -1){
              $(this).data('processed',"1");
              CKEDITOR.replace($(this).attr('id'), $(this).data('config'));
            }
          });
        }
      });
    };

    var changeId = function (obj){
        var o_id = obj.attr('id');
        var o_nm = obj.attr('name');
        var o_dt_id = obj.attr('data-section-id');
        var arr = {
            "id": o_id,
            "name": o_nm
        };

        for (var key in arr) {
          if (arr.hasOwnProperty(key)) {
              if (arr[key]){
                var temp = arr[key].split('_');
                // Loop thru only if array has more that 1 element after splitting
                if (temp.length > 1){
                    var c_id = temp.pop();
                    temp.push(c_id-1);
                }
                var val = temp.join('_');
                obj.attr(key, val);
              }
          }
        }
        if (o_dt_id){
            obj.attr("data-section-id", o_dt_id-1);
        }

    };

    var pullUp = function(s_id){
        // When a Section gets deleted this function reorders the elements
        $('div.section').each(function (){
            if (parseInt($(this).attr('data-section-id')) > s_id){
                $(this).find('*').each(function (){
                    changeId($(this));
                });
                changeId($(this));
            }
        });
    };

    var delSection = function(s_id){
        // This function deletes a give section
        if (s_id == 1){
            // TODO: Cannot delete main section display a message to user.
            return
        }

        sec_id --;

        $('div#sec' + '_' + s_id).remove();

        pullUp(s_id);
    };

    var resetSection = function(s_id){
        // This function resets values in a given section a give section
        var idtoreset = (s_id == 1) ? '': '_' + s_id;
        $('div#sec' + idtoreset).find('input.rep').val('');
    };

    var addSection = function(){
        // This function resets values in a given section a give section
        sec_id ++;
        var mainT = $(mainHtml);
        iId(mainT, true);
        mainT.insertBefore($('form #div_id_tags'));
        ckInit();
    };

    var iId = function (el, self){
        if (self){
            var o_id = el.attr('id');
            if (o_id) {
                var n_id = o_id + '_' + sec_id;
                el.attr('id', n_id);
            }
            if ($(el).attr('data-section-id')){
                $(el).attr('data-section-id', sec_id);
            }
        }

        el.find('*').each(function (){
            var o_id = $(this).attr('id');
            var o_nm = $(this).attr('name');
            if (o_id) {
                var n_id = o_id + '_' + sec_id;
                $(this).attr('id', n_id);
            }
            if (o_nm) {
                var n_nm = o_nm + '_' + sec_id;
                $(this).attr('name', n_nm);
            }
            if ($(this).attr('data-section-id')){
                $(this).attr('data-section-id', sec_id);
            }
        });
    };

    var funcs = {
        'del': delSection,
        'reset': resetSection,
        'add': addSection
    };

    $(document).on('click', '.sec_btn', function(){
        // Find the type of the button
        var btn = $(this).data('btnNm') ;
        var s_id = $(this).attr('data-section-id') ;
        if (btn == 'del' || btn == 'reset' || btn == 'add'){
            // Call the appropriate function
            if (s_id){
                funcs[btn](s_id);
            } else {
                funcs[btn]();
            }
        }
    });

    $(document).on('click', '.unlike, .like, .abusive', function(){
        // Find the type of vote
        var vote_type = $(this).data('type');
        var data_type = '';
        if (vote_type == 1) {
            data_type = 'likes';
        } else if(vote_type == 0) {
            data_type = 'unlikes';
        } else {
            data_type = 'abusive';
        }
        var parent = $(this).parent();
        var sec_id = parent.attr('sec_id');
        var article_id = parent.attr('article_id');
        var url = '/vote/';
        $.post(url, {'article': article_id, 'section': sec_id, 'vote_type': vote_type}, function(data){
            if (data.status == 'N'){
                console.log('Error casting vote');
            } else if (data.status == 'Y'){
                parent.children('span.'+data_type).text(data.data);
            }

        });

    });

    // Start of Menu
    var menu = $('#menu');

    function toggleHorizontal() {
        menu.find('.custom-can-transform').each(function(){
            $(this).toggleClass('pure-menu-horizontal');
        });
    }

    function toggleMenu() {
        // set timeout so that the panel has a chance to roll up
        // before the menu switches states
        if (menu.hasClass('open')) {
            setTimeout(toggleHorizontal, 500);
        }
        else {
            toggleHorizontal();
        }
        menu.toggleClass('open');
        $('#toggle').toggleClass('x');
    }

    function closeMenu() {
        if (menu.hasClass('open')) {
            toggleMenu();
        }
    }

    $('#toggle').on('click', function (e) {
        toggleMenu();
    });

    $(window).on('orientationchange, resize', function(){
        closeMenu();
    });

    // End of Menu

    // Get Cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings){
            if (!csrfSafeMethod(settings.type) && !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // End of Get Cookies

    // Modal popup
    $(function () {
        $('.popup-modal').magnificPopup({
            type: 'inline',
            preloader: false,
            focus: '#username',
            modal: true
        });
        $(document).on('click', '.popup-modal-dismiss', function (e) {
            e.preventDefault();
            $.magnificPopup.close();
        });
    });
    // End of Modal popup

    $('.trig').on('click', function(e){
        e.preventDefault();
        var temp = $(this).attr('id').split('_');
        var to_trigger = temp[temp.length-1];
        var offset = $(this).offset();
        var right = offset.left + $(this).width();
        right = right.toString();
        var top = offset.top + $(this).height();
        top = top.toString();
        var pos = {'right': right+'px', 'top': top+'px'};
        $('#'+to_trigger).slideToggle();
        $('#'+to_trigger).css(pos);

    });

    $('.s-trig').on('click', function(e){
        var this_id = $(this).data('sec-id');
        var text = $(this).text() == 'View Summary' ? 'Hide Summary' : 'View Summary';
        $('#summary_' + this_id).slideToggle();
        $(this).text(text);
    });

    $('.ajax-popup-link').magnificPopup({
      type: 'ajax'
    });

    $('.compare .inner tr > td > p > img + span').on('click', function(e){
        var inner = $('.compare .inner');
        var ind = $(this).attr('index');
        if (ind){
            var num = ind;
            inner.find('tr:eq('+ num +') > td > p > img + span').removeAttr('index');
        } else{
            var num = $(this).parent().parent().parent().index();
            inner.find('tr:eq('+ num +') > td > p > img + span').attr('index', num);
        }

        if ($(this).hasClass('only')){
            $(this).removeClass('only');
            //$(this).text($(this).attr('original'));
            inner.find('tr:eq('+ num +') > td > p > img + span').text($(this).attr('original'));

        } else {
            inner.find('tr:eq('+ num +') > td > p > img + span').addClass('only');
            var text = $(this).text();
            inner.find('tr:eq('+ num +') > td > p > img + span').attr('original', text);
            text = text.replace('only this', 'all');
            text = text + "'s";
            //$(this).text(text);
            inner.find('tr:eq('+ num +') > td > p > img + span').text(text);
        }

        inner.find('tr:not(:eq('+ num +'))').slideToggle();
    });

}());



    let pr_quant = 1;
    let price = 0;

    function total_price(pr, quan){
        $('.total-price').text( Math.round(pr * quan) );
    };


    function btn_Active(id){
        if( $('#optionpost')){
            $('#optionpost').remove();
        };
        $('.option-field').children().css({'background-color':'#eee', 'color':'#7359C6'});
        $('#' + id).css({'background-color':'#7359C6', 'border':'none', 'color':'#E1FF00'});
        price = $('a[data-id =' + id + ']').data('price');
        total_price(price, pr_quant);
        $('.option-field').append( '<input id="optionpost" type="text" style="display:none;" name="option" >');
        $('#optionpost').val(id);
        };

    function matt_glossy_Active(id){
        if( $('#mattpost')){
            $('#mattpost').remove();
        };
        $('.matt-field').children().css({'background-color':'#eee', 'color':'#7359C6'});
        $('#' + id).css({'background-color':'#7359C6', 'border':'none', 'color':'#E1FF00'});
        $('.matt-field').append( '<input id="mattpost" type="text" style="display:none;" name="matt_glossy" >');
        $('#mattpost').val(id);

    };



    function reply_click(clicked_id){
        pr_quant = 1;

        // ---------------------------------quantity section----------------------------

        if($('.modal-quantity')){
            $('.modal-quantity').remove();
            $('.quantity-unit').remove();
        };


        $('.quant-field').append('<input class="quantity-field text-center w-50 modal-quantity"  value="1" type="number"  name="quantity" max="50">');
        $('.quant-field').append( '<a class="quantity quantity-unit">'  + $('#'+ clicked_id).data('unit') +  ' </a> ');
        $('.quant-field').on("input", function(e) {
                 pr_quant = e.target.value;
                if (Number(e.target.value) > 50){
                    $('.quantity-field').val('50');
                    pr_quant = 50;
                }
                else if (Number(e.target.value) < .1 ) {
                    if ($('#'+clicked_id).data('float') === 'False') {
                        $('.quantity-field').val('0.1');
                        pr_quant = 0.1 ;
                   }
                   else{
                        $('.quantity-field').val('1');
                        pr_quant = 1 ;
                   }
                };
                total_price(price, pr_quant);

            });

       if ($('#'+clicked_id).data('float') === 'False') {
        $('.modal-quantity').attr( 'min', '0.1');
        $('.modal-quantity').attr( 'step', '0.1');
       }
       else{
       $('.modal-quantity').attr( 'min', '1');
       $('.modal-quantity').attr( 'step', '1');
       }
        // ---------------------------------------options--------------------------------------
        $('.option-field').empty();
        $('.' + clicked_id).each(function(index, elem){

            let radio_add = $('<button type="button"  ></button>');
            $(radio_add).attr('id', $(elem).data('id') );
            $(radio_add).attr('value', $(elem).data('id') );
            $(radio_add).attr('class', 'btn-option, my-1' );
            $(radio_add).css({'width':'100%', 'border-radius':'10px', 'color':'#7359C6', 'outline':'none', 'border': 'none'});
            $(radio_add).attr('onclick', 'btn_Active(this.id)' );


                //----------text for buttons-----------

            var text_label = ''
            if ( $(elem).data('width') !== '-' && $(elem).data('width') !== '' && $(elem).data('width') !== ' ' ){
             text_label += 'Ширина ' + $(elem).data('width');
            };
            if ( $(elem).data('sheet') !== '-' && $(elem).data('sheet') !== '' && $(elem).data('sheet') !== ' '  ){
             text_label += 'Размер листа ' + $(elem).data('sheet');
            };
            if ( $(elem).data('thicknes') !== '-' && $(elem).data('thicknes') !== '' && $(elem).data('thicknes') !== ' '  ){
             text_label += 'Толщина ' + $(elem).data('thicknes');
            };
            if ( $(elem).data('color') !== '-' && $(elem).data('color') !== '' && $(elem).data('color') !== ' '  ){
                text_label += 'Цвет ' + $(elem).data('color');
               };

            if ( $(elem).data('power') !== '-' && $(elem).data('power') !== '' && $(elem).data('power') !== ' '  ){
                text_label += 'Мощность ' + $(elem).data('power');
               };


            text_label += ' по цене ' + $(elem).data('price') + ' руб. за ' + $('#'+ clicked_id).data('unit')
            $(radio_add).text(text_label);




            //========================================set default========
            $('.option-field').append( radio_add );
            if ( $(elem).data('default') === 'True'  ) {
                btn_Active($(elem).data('id'));
                };
        });


        if ( $('#'+ clicked_id).data('matt') === 'True') {
            let mat = $('<button type="button" id="matt"  >Матовая</button>');
            $(mat).css({'width':'50%', 'border-radius':'10px', 'color':'#7359C6', 'outline':'none', 'border': 'none'});
            $(mat).attr('onclick', 'matt_glossy_Active(this.id)' );


            let glossy = $('<button type="button" id="glossy"  >Глянцевая</button>');
            $(glossy).css({'width':'50%', 'border-radius':'10px', 'color':'#7359C6', 'outline':'none', 'border': 'none'});
            $(glossy).attr('onclick', 'matt_glossy_Active(this.id)' );


            $('.matt-field').append( mat );
            $('.matt-field').append( glossy );
            matt_glossy_Active('matt')


        };

      $('.modal-title').text( $('#'+ clicked_id).data('product'));
      $('.prw-sel').attr( 'src', '/' + $('#'+ clicked_id).data('prw'));
      if($('#'+ clicked_id).data('producer') !== '-' && $('#'+ clicked_id).data('producer') !== '' && $('#'+ clicked_id).data('producer') !== ' '){
        $('.producer').text('Произодитель:   ' + $('#'+ clicked_id).data('producer'));
        };

    };


    
            $( document ).ready(function() {


                // var obj_json = $.parseJSON(cat_json);


                // $.each(cat_json, function(key, val){

                // })




            });



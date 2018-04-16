$(document).ready(function(){
  $('form').submit(function(event){
    event.preventDefault();
    var $form = $(this), url = $form.attr('action'), method=$form.attr('method');
    var reader = new FileReader();
    reader.readAsDataURL($form.find('input[type=file]')[0].files[0]);
    console.log($form.find('input[type=file]')[0].files[0]);
    console.log(reader);
    reader.onload = function(){
      $.ajax({
        'url': url,
        'method': method,
        'data': {'file': reader.result},
        'beforeSend': function(){
          $form.find('input[type=submit]').prop('disabled', true)
                                          .val('Working...');
        },
        'complete': function(data){
          console.log(data.responseJSON.result);
          $form.find('input[type=submit]').val('Submit')
                                          .prop('disabled', false);
          $('#result h1').html(data.responseJSON.result);
          $('#result').fadeIn();
        },
        'error': console.log
      });
    }
  });
});

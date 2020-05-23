$(function () {
    //Máscara de telefone
    $(document).ready(function(){
      $(".telefone").inputmask("(99) 9999[9]-9999",
      { 
        showMaskOnFocus: true      
      });
    });
  })
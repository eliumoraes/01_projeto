$(function () {
    //Máscara de telefone
    $(document).ready(function(){
      $(".telefone").inputmask("(99) 9999-9999[9]",
      { 
        showMaskOnFocus: true      
      });
    });
  })
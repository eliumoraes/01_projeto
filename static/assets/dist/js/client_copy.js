function clientCopy() {
    /* Get the text field */
    var copyText = document.getElementById("last_location");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
  
    /* Chama um toast e exibe mensagem dizendo o que foi copiado! */
    toastr.info("Copiado: " + copyText.value);
  }
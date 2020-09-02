function clientCopy(id='') {
    /* Get the text field */
    var copyText = document.getElementById(("last_location").concat(id));

    if (id != ''){
      copyText.style.display = "block";
    }
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/
  
    /* Copy the text inside the text field */
    document.execCommand("copy");

    if (id != ''){
      copyText.style.display = "none";
    }
  
    /* Chama um toast e exibe mensagem dizendo o que foi copiado! */
    toastr.info("Copiado: <br>" + copyText.value);
  }
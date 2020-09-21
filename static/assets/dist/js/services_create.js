//Muda o nome do botão de "Escolha" para a função escolhida.
function replaceButtonText(buttonId, text)
{
  if (document.getElementById)
  {
    var button=document.getElementById(buttonId);
    if (button)
    {
      if (button.childNodes[0])
      {
        button.childNodes[0].nodeValue=text;
      }
      else if (button.value)
      {
        button.value=text;
      }
      else //if (button.innerHTML)
      {
        button.innerHTML=text;
      }
    }
  }
}



//Inicío do padrão de criação dos elementos

serviceList = []

function serviceElement(textIn=''){
  buttonH = document.getElementById('buttonHead');
  elType = buttonH.childNodes[0].nodeValue;
  serviceBody = document.getElementById('service_body');
  id = (Math.floor(Math.random() * 99999) + Math.floor(Math.random() * 10)).toString(16)  

  if (elType == 'Texto Linha'){      
    serviceIcon = buttonH = document.getElementById('serviceIcon').childNodes[0]
    serviceText = document.getElementById('inlineFormInput').value

    dic = {type: "SimpleText", value: serviceText, icon: serviceIcon.classList.value, id: id}

    lineText = '\
      <div class="input-group mb-3 col-11" id="el_'+id +'">\
        <div class="input-group-prepend">\
            <span class="input-group-text">' + serviceIcon.outerHTML +'</span>\
        </div>\
        <input name="service_name" type="text" class="form-control" placeholder="'+ serviceText +'">\
      </div>\
      <div class="col-1" id="x_'+id +'">\
      <button onclick="removeEl(\''+id +'\')" type="button" class="btn btn-secondary btn-block"><i class="far fa-window-close"></i></button>\
      </div>\
    ';

    serviceBody.innerHTML += lineText;

    serviceList.push(dic)
  }

  if(textIn=='' || textIn=='<p><br></p>'){
    textIn ='\
    <h5>Observação:</h5>\
    <p>Este campo poderá ser utilizado para inserir textos de observação ao inserir o serviço no cliente.</p>\
    ';
  }

  if (elType == 'Texto Multilinha (fixo)'){
    dic = {type: "MultiText", value: textIn, icon: "None", id: id}
    serviceText = '\
    <div class="col-12" id="el_'+id +'">\
      <div class="callout callout-info">\
      <a onclick="removeEl(\''+id +'\')"><i class="far fa-window-close float-right"></i></a>\
      ' +textIn + '\
      </div>\
    <\div>'

    serviceBody.innerHTML += serviceText;
    serviceList.push(dic)
  }

}

// Função de deleção dos elemntos:
function removeEl(id){
  el = document.getElementById('el_'+id);
  xx = document.getElementById('x_'+id);
  if(el!=null){
    el.remove();
  }
  if(xx!=null){
    xx.remove();
  }  
  serviceList = serviceList.filter(function( obj ) {
    return obj.id !== id;
  });
}


//Textarea:
function MultiStart() {
  // Summernote
  $('#multiText').summernote({
    toolbar: [
      ['style', ['style']],
      ['font', ['bold', 'underline', 'clear']],
      ['fontname', ['fontname']],
      ['color', ['color']],
      ['para', ['ul', 'ol', 'paragraph']],
      ['table', ['table']],
      // ['insert', ['link', 'picture', 'video']],
      ['view', ['fullscreen', 'codeview']],
    ],
  })
}

//Pegar conteúdo:
function getCont(){
  cont = $('#multiText').summernote('code');
  serviceElement(cont);
}

//Limpa o construct:
function clearConstruct(){
  $('#multiText').summernote('destroy');
  x = document.getElementById('construct')
  while(x.childNodes.length>0){
    x.removeChild(x.lastChild);
  }
  buttonContent = '\
  <div class="col-3 mb-3">\
    <div class="btn-group btn-block">\
        <button type="button" id="buttonHead" class="btn btn-primary">Escolha</button>\
        <button type="button" class="btn btn-primary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown">\
        </button>\
        <div class="dropdown-menu">\
          <a class="dropdown-item" onclick="constructLinha(\'buttonHead\', \'Texto Linha\')">Texto Linha</a>\
          <a class="dropdown-item" onclick="constructMulti(\'buttonHead\', \'Texto Multilinha (fixo)\')">Texto Multilinha (fixo)</a>\
        </div>\
  </div>\
  ';
  x.innerHTML += buttonContent;
}

//Elimina o multiText: $('#multiText').summernote('destroy');

function constructLinha(buttonId, text){
  clearConstruct();
  replaceButtonText(buttonId, text);  
  construct = document.getElementById('construct');
  prep = '\
  <div class="col-1 mb-3">\
    <button id="serviceIcon" class="btn btn-primary btn-block" data-icon="fas fa-home" role="iconpicker" enabled></button>\
  </div>\
  <div class="col-7 mb-3">\
    <input type="text" class="form-control" id="inlineFormInput" placeholder="Nome do campo">\
  </div>\
  <div class="col-1 mb-3">\
    <button onclick="serviceElement()" class="btn btn-primary btn-block"><i class="fas fa-plus-square"></i></button>\
  </div>\
  ';
  construct.innerHTML += prep;
  $('#serviceIcon').iconpicker();

}

function constructMulti(buttonId, text){
  clearConstruct();
  replaceButtonText(buttonId, text);  
  construct = document.getElementById('construct');
  prep = '\
  <div class="col-12">\
      <textarea id="multiText" name="" class="form-control" rows="10"></textarea>\
  </div>\
  <div class="col-2">\
      <button onclick="getCont()" class="btn btn-primary"><i class="fas fa-plus-square"></i>&nbsp;&nbsp;&nbsp;Inserir</button>\
  </div>\
  ';
  construct.innerHTML += prep;
  MultiStart();

}

/**
 * 
 * Testes de envio de dados com Javascript
 */


$("#friend-form").submit(function (e) {
  // preventing from page reload and default actions
  e.preventDefault();
  // serialize the data for sending the form data.
  var serializedData = JSON.stringify(serviceList)
  // make POST ajax call
  $.ajax({
      type: 'POST',
      url: "{% url 'services_create' %}",
      data: serializedData,
      success: function (response) {
        console.log(JSON.parse(response["instance"]))
          // on successfull creating object
          // 1. clear the form.
          // $("#friend-form").trigger('reset');
          // // 2. focus to nickname input 
          // $("#id_nick_name").focus();

          // display the newly friend to table.
          // var instance = JSON.parse(response["instance"]);
          // var fields = instance[0]["fields"];
          // $("#my_friends tbody").prepend(
          //     `<tr>
          //     <td>${fields["nick_name"]||""}</td>
          //     <td>${fields["first_name"]||""}</td>
          //     <td>${fields["last_name"]||""}</td>
          //     <td>${fields["likes"]||""}</td>
          //     <td>${fields["dob"]||""}</td>
          //     <td>${fields["lives_in"]||""}</td>
          //     </tr>`
          // )
      },
      error: function (response) {
          // alert the error if any error occured
          console.log(JSON.parse(response["instance"]))
          alert(response["responseJSON"]["error"]);
      }
  })
})




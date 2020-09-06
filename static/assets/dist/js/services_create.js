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

function serviceElement(){
  buttonH = document.getElementById('buttonHead');
  elType = buttonH.childNodes[0].nodeValue;
  serviceBody = document.getElementById('service_body');

  if (elType == 'Texto Linha'){
    id = (Math.floor(Math.random() * 99999) + Math.floor(Math.random() * 10)).toString(16)    
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

  if (elType == 'Texto Multilinha (fixo)'){
    serviceText = '\
    <div class="col-12">\
      <div class="callout callout-info">\
        <h5>Observação:</h5>\
        \
        <p>Este campo poderá ser utilizado para inserir textos de observação ao inserir o serviço no cliente.</p>\
      </div>\
    <\div>'

    serviceBody.innerHTML += serviceText;
  }

}

// Função de deleção dos elemntos:
function removeEl(id){
  el = document.getElementById('el_'+id);
  xx = document.getElementById('x_'+id);
  el.remove();
  xx.remove();
  serviceList = serviceList.filter(function( obj ) {
    return obj.id !== id;
  });
}
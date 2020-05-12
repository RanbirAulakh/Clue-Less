$('label[for=id_private_key]').remove();
$('#id_private_key').remove();
$('#id_type').change(function () {
   let value = $(this).val();
   if (value == "Private") {
       $('#id_private_key').remove();
       $('<div class="row"> <div class="col-md-12"> <div class="input-group" id="password_input">\n' +
           '  <input type="text" class="form-control" id="id_private_key" name="private_key" required>\n' +
           '  <div class="input-group-append">\n' +
           '    <a id="generateKey"  class="btn btn-outline-secondary" type="button">Generate Key</a>' +
           '  </div></div><label style="">Please share this key with your friends!</label>\n' +
           '</div></div>').insertBefore('#submitBtn');
   } else {
       $('#password_input').remove();
   }
});

$(document).on('click', '#generateKey', function(){
  var pass = randomPassword(5);
  console.log(pass);
  $('#id_private_key').val(pass);
});

function randomPassword(length) {
    var chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP1234567890";
    var pass = "";
    for (var x = 0; x < length; x++) {
        var i = Math.floor(Math.random() * chars.length);
        pass += chars.charAt(i);
    }
    return pass;
}

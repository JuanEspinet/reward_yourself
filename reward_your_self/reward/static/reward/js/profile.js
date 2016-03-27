$(document).ready(function(){
  var $profileUpdate = $('#update');
  $profileUpdate.click(updateProfile);
});

function getFieldData(){
  // parses form data and returns as an object
  var $formFields = $('.profile input'), // cache all form fields
      csrf = $('[name="csrfmiddlewaretoken"]').val(),
      formData = {
        csrfmiddlewaretoken: csrf,
        active_group: $('#active_group').val()
      };
  for (var i = 0; i < $formFields.length; i++){
    var current = $formFields[i];
    console.log(current);
    // get contents of each field that is not a button
    if (current.type != 'button') {
      formData[current.name] = current.value;
    }
  }
  return formData;
}

function updateProfile(event){
  // calls Django view to update all profile fields
  // will only update fields for which data are provided
  var formData = getFieldData();
  event.preventDefault();
  $.ajax({
    url: '/profile_update/',
    data: formData,
    method: 'POST'
  }).success(function(data, status, jqXHR){
    console.log(data);
  });
}

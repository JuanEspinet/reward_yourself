$(document).ready(function(){
  $('#search').click(inviteUser);
});

function getInviteUsername(){
  // retreives contents of username field
  var username = $('#username');
  return username.val();
}

function inviteUser(){
  // sends an invite user request
  var formData = addCSRF({
    username : getInviteUsername()
  });
  $.ajax({
    url: '/invite_attempt/',
    data: formData,
    method: 'POST'
  }).success(function(data, status, jqXHR){
    // TODO: fill in success processing
    console.log(data);
  }).error(function(data, status, jqXHR){
    // TODO: fill in failure processing
    console.log(data);
  });
}

function acceptInvite(){
  // processes a click on an accept invite button
}

function rejectInvite(){
  // processes a click on a reject invite button
}

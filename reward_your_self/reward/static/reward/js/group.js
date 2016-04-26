$(document).ready(function(){
  $('#search').click(inviteUser);
  $('.accept_reject').click(decideInvite);
});

function getInviteUsername(){
  // retreives contents of username field
  var username = $('#username');
  return username.val();
}

function inviteUser(event){
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

function decideInvite(event){
  // processes a click on an accept/reject invite button
  var groupPK = $(event.target).parent().attr('id'),
      reqType = $(event.target).attr('name'),
      formData = addCSRF({
        group_pk : groupPK
      }),
      settings = {
        url: '/' + reqType + '/',
        data: formData,
        method: 'POST'
      };
  $.ajax(settings).success(function(data, status, jqXHR){
    // TODO: fill in success processing
    console.log(data);
    window.location = '/groups/';
  }).error(function(data, status, jqXHR){
    // TODO: fill in failure processing
    console.log(data);
  });
}

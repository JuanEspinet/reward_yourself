$(document).ready(function(){
  var $logOutButton = $('#logout');
  $logOutButton.click(logoutButtonPush);
});

function logoutButtonPush(){
  window.location = '/logout_request/';
}

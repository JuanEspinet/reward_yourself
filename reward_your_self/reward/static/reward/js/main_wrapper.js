$(document).ready(function(){
  var $logOutButton = $('#logout');
  $logOutButton.click(logoutButtonPush);
});

function logoutButtonPush(){
  window.location = '/logout_request/';
}

function changePoints(newPoints){
  // changes the displayed point total
  var $points = $('#point_total');
  $points.text(newPoints);
  return $points;
}

function addCSRF(data){
  // gets the csrf token for a page and attaches it to a set of data
  var csrf = $('[name="csrfmiddlewaretoken"]').val();
  data.csrfmiddlewaretoken = csrf;
  return data;
}

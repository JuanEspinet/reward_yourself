$(document).ready(function(){
  $('#add_point').click(addPoint);
  $('#get_reward').click(goToRewards);
});

function goToRewards(){
  window.location = '/rewards/';
}

function addPoint(){
  $.ajax({
    url : '/add_point/',
    method : 'GET',
  }).success(function(){
    window.location = '/main/';
  });
}

$(document).ready(function(){
  $('#add_point').click(addPoint);
  $('#get_reward').click(goToRewards);
  setProgressBar();
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

function percentProgress(){
  return (totalPoints / pointCost) * 100;
}

function setProgressBar(){
  var bar = document.getElementById('inner_bar');
  bar.style.width = String(percentProgress()) + '%';
}

$(document).ready(function(){
  $('.reward_button').click(redeemReward);
});

function redeemReward(event){
  // handler for redemption button clicks
  var $rewardButton = $(event.target),
      rewardId = event.target.id,
      data = addCSRF({reward_id : rewardId});
  $.ajax({
    url: '/redeem_reward/',
    data: data,
    method: 'POST'
  }).success(function(){
      window.location = '/rewards/';
    }
  );
}

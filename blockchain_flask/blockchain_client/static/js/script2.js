document.querySelector('.img__btn').addEventListener('click', function () {
  document.querySelector('.cont').classList.toggle('s--signup');
});


document.querySelector('.submit-xD').addEventListener('click', function () {
  document.querySelector('.cont').classList.toggle('s--signup');
});

var $loader = $(".sign-up");
var $btnDone = $loader.find(".done");
var $loadingMessage = $loader.find(".loader-message");


$(document).ready(function () {
  $btnDone.click(function () {
    $('.success').fadeOut(500);
  });
});
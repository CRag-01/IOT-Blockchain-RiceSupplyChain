document.querySelector('.img__btn').addEventListener('click', function () {
  document.querySelector('.cont').classList.toggle('s--signup');
});


document.querySelector('.submit-xD').addEventListener('click', function () {
  document.querySelector('.cont').classList.toggle('s--signup');
});

// SUCCESS MODAL PART 
var $loader = $(".sign-up");
var $btnDone = $loader.find(".done");
var $loadingMessage = $loader.find(".loader-message");
var $btnRetry = $loader.find(".retry");
var $btnCancel = $loader.find(".cancel");

$(document).ready(function () {
  $btnDone.click(function () {
    $('.success').fadeOut(500);
  });
});

$(document).ready(function () {
  $btnCancel.click(function () {
    $('.error').fadeOut(500);
  });
});
$('#login').click(function (evt) {
  $('#form-login').dialog(
    {
			  width: 600,
			  modal: true,
	  }
	);
	$('#prevSlide').hide();
  $('#nextSlide').hide();
});

var currentStep = 1;

function showHideButtons () {
  if (currentStep <= 1) {
    $("#prevSlide").hide();
    currentStep = 1;
  } else {
    $("#prevSlide").show();
  }
  
  if (currentStep >= 5) {
    $("#nextSlide").hide();
    currentStep = 5;
  } else {
    $("#nextSlide").show();
  }
}

$('#register').click(function (evt) {
  $('#form-register').dialog(
    {
			  width: 800,
			  height: 450,
			  modal: true,
			  resizable: false,
	  }
	);
	
	//$('fieldset').hide();
  //$('#step1').show();
  
  showHideButtons ();
});

$('#nextSlide').click(function (evt) {
  console.log("okay");
  var newMargin = -800 * currentStep;
  currentStep += 1;
  $('.pop-up-container').css("margin-left", newMargin + "px");
  showHideButtons();  
});

$('#prevSlide').click(function (evt) {
  currentStep -= 1;
  var newMargin = -800 * (currentStep - 1);
  $('.pop-up-container').css("margin-left", newMargin + "px");
  showHideButtons();  
});

$('.changeStep').click(function (evt) {
  var st = evt.currentTarget.id.split('stepMoveTo')[1];
  currentStep = parseInt(st);
  var newMargin = -800 * (currentStep - 1);
  console.log(newMargin);
  $('.pop-up-container').css("margin-left", newMargin + "px");
});
/*
$('input').live('keydown', function(evt) {
  
  evt.preventDefault();
});*/

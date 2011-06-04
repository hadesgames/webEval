$('#login').click(function (evt) {
  $('#form-login').dialog(
    {
			  width: 600,
			  modal: true,
	  }
	);
	
  $('#form-login').load('/api/login_form/');
	$('#prevSlide').hide();
  $('#nextSlide').hide();
});

currentStep = 1;

function showHideButtons () {
  console.log("okay");
  console.log(currentStep);
  if (currentStep <= 1) {
    $("#prevSlideButton").hide();
    currentStep = 1;
  } else {
    $("#prevSlideButton").show();
  }
  
  if (currentStep >= 5) {
    $("#nextSlideButton").hide();
    currentStep = 5;
  } else {
    $("#nextSlideButton").show();
  }
};

$('#register').click(function (evt) {
  console.log("okay");
  $('#form-register').dialog({
        width: 800,
        height: 450,
        modal: true,
        resizable: false,
    }
  );
  $('#form-register').load('/api/register_form/');
  showHideButtons ();
});


function nextSlide () {
  console.log("next");
  var newMargin = -800 * currentStep;
  currentStep += 1;
  $('.pop-up-container').css("margin-left", newMargin + "px");
  showHideButtons();
}

function prevSlide () {
  console.log("prev");
  currentStep -= 1;
  var newMargin = -800 * (currentStep - 1);
  $('.pop-up-container').css("margin-left", newMargin + "px");
  showHideButtons();  
}

function changeStep(st) {
  //var st = evt.currentTarget.id.split('stepMoveTo')[1];
  currentStep = parseInt(st);
  var newMargin = -800 * (currentStep - 1);
  console.log(newMargin);
  $('.pop-up-container').css("margin-left", newMargin + "px");
  showHideButtons();
}


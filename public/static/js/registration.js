function validateEmail () {
	var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	var address = document.getElementById('form_email').value;
	console.log(address);
	if(reg.test(address) == false) {
		document.getElementById('form_email_hint').innerHTML = 'Invalid email address.';
		document.getElementById('form_email_hint').style.color = "#FF0000";
	} else {
		document.getElementById('form_email_hint').innerHTML = 'Okay';
		document.getElementById('form_email_hint').style.color = "#666666";
	}
}

function validateUsername () {
	var reg = /^([A-Za-z0-9_\.])+$/;
	var address = document.getElementById('form_username').value;
	console.log(address);
	if (reg.test(address) == false) {
		document.getElementById('form_username_hint').innerHTML = 'Only letters, digits, _ and . allowed';
		document.getElementById('form_username_hint').style.color = "#FF0000";
	}
	 else {
		document.getElementById('form_username_hint').innerHTML = 'Okay';
		document.getElementById('form_username_hint').style.color = "#666666";
	}
}

function validatePassword () {
	var value1 = document.getElementById('form_password').value;
	var value2 = document.getElementById('form_password2').value;
	
	if (value1 != value2) {
		document.getElementById('form_password_hint').innerHTML = 'Passwords don\'t match';
		document.getElementById('form_password_hint').style.color = "#FF0000";
	} else if (value1.length < 6) {
		document.getElementById('form_password_hint').innerHTML = 'At least 6 characters';
		document.getElementById('form_password_hint').style.color = "#FF0000";
	} else {
		document.getElementById('form_password_hint').innerHTML = 'Okay';
		document.getElementById('form_password_hint').style.color = "#666666";
	}
}

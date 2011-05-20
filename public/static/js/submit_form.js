function displayContestsForProblem() {
	problem = document.getElementById('form_task').value;
	$('#form_round').html( '&nbsp;' ).load('/api/get_rounds_for_problem/?problem_id='+problem);
	document.getElementById('field_round').style.display = 'block';
	document.getElementById('field_compiler').style.display = 'block';
}

function changeCompiler(){
	var f = document.getElementById('form_solution');
	var compiler = document.getElementById('form_compiler');
	if (document.getElementById('field_compiler').style.display == 'none') {
		document.getElementById('field_compiler').style.display = 'block';
	}

    // we simply map file extensions to hard-coded compiler IDs
    var k = -1;
    for (var i = f.value.length - 1; 0 <= i; i--) {
        if ('.' == f.value.charAt(i)) {
            k = i;
            break;
        }
    }
    var ext = f.value.substring(k + 1).toLowerCase();
    if ('adb' == ext || 
    	'bas' == ext ||
    	'boo' == ext ||
    	'c' == ext || 
    	'cpp' == ext || 
    	'cs' == ext ||
    	'ml' == ext ||
    	'pas' == ext ||     	 
    	'php' == ext || 
    	'pike' == ext ||
    	'pl' == ext ||
    	'py' == ext ||
    	'rb' == ext ||
    	'tcl' == ext) {
        compiler.value = ext;
    }
    else {
        alert('Warning! I cannot choose a compiler for this extension ');
        compiler.value = '-';
    }
}

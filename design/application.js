$('document').ready(function() {
  $('#header_user').click(function(evt) {
    $('#header_user_dropdown').toggle('slow');
    evt.preventDefault();
  });
})

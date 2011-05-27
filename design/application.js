$('document').ready(function() {
  $('#sliding-menu-button').click(function() {
    console.log("click");
    $("#sliding-menu-panel").toggle("slow");
  });
})
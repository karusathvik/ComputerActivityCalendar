
let curr_list = jQuery("#curr-results");
function render_results (results) {
    console.log(results);
    //add to curr_list a little later

}

$("#activity-form").on("submit", function (event) {
   event.preventDefault();
   let cd = jQuery("#activity-date").val();
   console.log(cd);
   //change the user id later
   $.ajax({
       url: "api/display",
       method: "GET",
       data: {user_id: "1", curr_date: cd},
       success: render_results
   });
});
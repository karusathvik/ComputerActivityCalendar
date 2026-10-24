
let curr_list = $("#curr-results");
function render_results (results) {
    console.log(results);
    curr_list.empty();
    $("#the-date-info").text(results[0]["recorded_at"].split()[0]);
    for (let i = 0; i < results.length; ++i) {
        let curr_record = $("<li>").text(results[i]["app"] + ": " + results[i]["title"]
        + " on:" + results[i]["recorded_at"]);
        curr_list.append(curr_record);
    }
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

//added utility for next / prev button but for now they do not do anything
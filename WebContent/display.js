const SAMPLE_MS = 5 * 60 * 1000;
const PIXELS_PER_MINUTE = 1.5;
let selectedDate = "";
let pendingRequest = null;
let generation = 0;

function dateKey(date) {
    return date.getFullYear() + "-" + String(date.getMonth() + 1).padStart(2, "0") + "-" + String(date.getDate()).padStart(2, "0");
}

function coalesce(records) {
    const ordered = records.map(record => ({...record, time: new Date(record.recorded_at.replace(" ", "T"))}))
        .filter(record => !isNaN(record.time)).sort((a, b) => a.time - b.time);
    const blocks = [];
    ordered.forEach(record => {
        const last = blocks[blocks.length - 1];
        if (last && last.app === record.app && record.time - last.last <= SAMPLE_MS + 60000) {
            last.last = record.time;
            last.count++;
            last.observations.push({time: record.time, title: record.title});
        } else {
            blocks.push({app: record.app, title: record.title, start: record.time, last: record.time, count: 1, observations: [{time: record.time, title: record.title}]});
        }
    });
    blocks.forEach((block, index) => {
        block.end = new Date(Math.min(+block.last + SAMPLE_MS, blocks[index + 1] ? +blocks[index + 1].start : Infinity));
    });
    return blocks;
}

function clock(date) {
    return date.toLocaleTimeString([], {hour: "numeric", minute: "2-digit"});
}

function updateNow() {
    const now = new Date();
    $("#now-line").prop("hidden", selectedDate !== dateKey(now)).css("top", (now.getHours() * 60 + now.getMinutes()) * PIXELS_PER_MINUTE);
}

function renderResults(records) {
    const blocks = coalesce(records);
    const events = $("#events").empty();
    const colors = [["#2563eb", "#e8f0fe"], ["#188038", "#e6f4ea"], ["#9334e6", "#f3e8fd"], ["#c26401", "#fef1db"]];
    let cluster = [];
    let clusterBottom = -1;
    let laneEnds = [];
    function finishCluster() {
        cluster.forEach(layout => layout.lanes = laneEnds.length);
        cluster = [];
        laneEnds = [];
    }
    const layouts = blocks.map(block => {
        const top = (block.start.getHours() * 60 + block.start.getMinutes() + block.start.getSeconds() / 60) * PIXELS_PER_MINUTE;
        const height = Math.min(1440 * PIXELS_PER_MINUTE - top, Math.max(32, (block.end - block.start) / 60000 * PIXELS_PER_MINUTE));
        if (top >= clusterBottom) finishCluster();
        let lane = laneEnds.findIndex(end => end <= top);
        if (lane === -1) lane = laneEnds.length;
        laneEnds[lane] = top + height;
        const layout = {block, top, height, lane};
        cluster.push(layout);
        clusterBottom = Math.max(...laneEnds);
        return layout;
    });
    finishCluster();
    layouts.forEach(({block, top, height, lane, lanes}) => {
        const hash = Array.from(block.app || "").reduce((sum, char) => sum + char.charCodeAt(0), 0);
        const [accent, bg] = colors[hash % colors.length];
        const element = $("<article>").addClass("event").css({top, height, left: (lane * 100 / lanes) + "%", width: "calc(" + (100 / lanes) + "% - 5px)", "--accent": accent, "--bg": bg});
        const details = block.observations.map(observation => `${clock(observation.time)} — ${observation.title || "Untitled"}`).join("\n");
        const description = `${block.app}\n${clock(block.start)}–${clock(block.end)} · ${block.count} observations · estimated duration\n\n${details}`;
        element.attr({title: description, tabindex: 0, "aria-label": description});
        element.append($("<strong>").text(block.app), $("<small>").text(clock(block.start) + "–" + clock(block.end)));
        events.append(element);
    });
    $("#empty-state").prop("hidden", blocks.length !== 0);
    $("#summary").text(`${blocks.length} activity blocks · ${records.length} observations`);
    updateNow();
}

function refreshActivities(scrollToDay = false) {
    if (!selectedDate || pendingRequest) return;
    const currentGeneration = generation;
    $("#refresh-status").removeClass("error").text("Refreshing…");
    pendingRequest = $.ajax({
        url: "api/display", method: "GET", dataType: "json", cache: false, timeout: 10000,
        data: {user_id: "1", curr_date: selectedDate},
        success: function (results) {
            if (currentGeneration !== generation) return;
            renderResults(results);
            $("#refresh-status").text("Auto-refresh every 30 seconds");
            $("#last-updated").text("Updated " + clock(new Date()));
            if (scrollToDay) {
                const first = results.length ? new Date(results[0].recorded_at.replace(" ", "T")) : null;
                const minute = selectedDate === dateKey(new Date()) ? new Date().getHours() * 60 : first ? first.getHours() * 60 : 8 * 60;
                $("#day-scroll").scrollTop(Math.max(0, (minute - 30) * PIXELS_PER_MINUTE));
            }
        },
        error: function (xhr, status) {
            if (status !== "abort" && currentGeneration === generation) $("#refresh-status").addClass("error").text("Couldn't refresh. Keeping the last loaded results.");
        },
        complete: function () { if (currentGeneration === generation) pendingRequest = null; }
    });
}

function selectDate() {
    const date = $("#activity-date").val();
    if (!date) return;
    generation++;
    if (pendingRequest) pendingRequest.abort();
    pendingRequest = null;
    const changed = selectedDate !== date;
    selectedDate = date;
    $("#the-date-info").text(new Date(date + "T12:00:00").toLocaleDateString([], {weekday: "long", month: "long", day: "numeric", year: "numeric"}));
    if (changed) {
        $("#events").empty();
        $("#summary, #last-updated").text("");
        $("#empty-state").prop("hidden", true);
    }
    updateNow();
    refreshActivities(changed);
}

for (let hour = 0; hour < 24; hour++) {
    $("#hours").append($("<div>").addClass("hour").css("top", hour * 60 * PIXELS_PER_MINUTE).append($("<span>").text((hour % 12 || 12) + (hour < 12 ? " AM" : " PM"))));
}
$("#activity-form").on("submit", function (event) { event.preventDefault(); selectDate(); });
$("#refresh").on("click", function () { refreshActivities(); });
$("#prev, #next").on("click", function () {
    const date = new Date(selectedDate + "T12:00:00");
    date.setDate(date.getDate() + (this.id === "next" ? 1 : -1));
    $("#activity-date").val(dateKey(date));
    selectDate();
});
$("#today").on("click", function () { $("#activity-date").val(dateKey(new Date())); selectDate(); });
document.addEventListener("visibilitychange", function () { if (!document.hidden) refreshActivities(); });
setInterval(function () { updateNow(); if (!document.hidden) refreshActivities(); }, 30000);
$("#activity-date").val(dateKey(new Date()));
selectDate();

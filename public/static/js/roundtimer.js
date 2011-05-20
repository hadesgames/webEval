var timers = {};

function relativeTime(timerId) {
    var now = new Date();

    var diff = timers[timerId].startTime.getTime() +
               timers[timerId].timeDifference -
               now.getTime();
    diff = (diff - diff % 1000) / 1000;

    var message = "";
    if (diff > 0) {
        // count down to round start
        message = "until round starts.";
        setTimeout("updateTime(\"" + timerId + "\")", 1000);
    } else if (diff == 0) {
        // refresh page
        setTimeout('document.location.reload(true)',
            1000 + 4000 * Math.random());
        return "";
    } else if (diff + timers[timerId].duration > 0) {
        // count down to round end
        diff += timers[timerId].duration;
        message = "until round ends.";
        setTimeout("updateTime(\"" + timerId + "\")", 1000);
    } else if (diff + timers[timerId].duration == 0) {
        // refresh page
        setTimeout('document.location.reload(true)',
            1000 + 4000 * Math.random());
        return "";
    } else {
        // round is over
        return "Runda s-a încheiat.";
    }

    var seconds = diff % 60;
    diff = (diff - seconds) / 60;
    var minutes = diff % 60;
    diff = (diff - minutes) / 60;
    var hours = diff % 24;
    diff = (diff - hours) / 24;
    var days = diff;

    var show = "";
    var unitsToShow = timers[timerId].units;
    var firstFound = false;

    if (days > 0 && unitsToShow > 0) {
        if (!firstFound)
            firstFound = true;
        if (days == 1)
            show += "one day ";
        else
            show += days + " days ";
    }
    if (firstFound)
        --unitsToShow;
    if (hours > 0 && unitsToShow > 0) {
        if (!firstFound)
            firstFound = true;
        if (hours == 1)
            show += "one hour ";
        else
       show += hours + " hours ";
    }
    if (firstFound)
        --unitsToShow;
    if (minutes > 0 && unitsToShow > 0) {
        if (!firstFound)
            firstFound = true;
        if (minutes == 1)
            show += "one minute ";
        else
            show += minutes + " minutes ";
    }
    if (firstFound)
        --unitsToShow;
    if (seconds > 0 && unitsToShow > 0) {
        if (!firstFound)
            firstFound = true;
        if (seconds == 1)
            show += "one second ";
        else
            show += seconds + " seconds ";
    }

    show = show.substring(0, 1).toUpperCase() + show.substring(1);

    show = "<strong>" + show + "</strong>";
    if (timers[timerId].showMessage == true)
        show += message;
    return show;
}

function updateTime(timerId) {
    $(timerId).innerHTML = relativeTime(timerId);
}

function newRoundTimer(timerId, serverTime, startTime,
                        duration, units, showMessage) {
    timers[timerId] = {};
    timers[timerId].timeDifference = (new Date()).getTime() -
                                     (new Date(serverTime)).getTime();
    timers[timerId].startTime = new Date(startTime);
    timers[timerId].duration = duration * 3600;
    timers[timerId].units = units;
    timers[timerId].showMessage = showMessage;
    updateTime(timerId);
}

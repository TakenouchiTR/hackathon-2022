function getLastItem(path) {
    path.substring(path.lastIndexOf('/') + 1)
}

function onEditJudgeClick(appName) {
    competitionName = document.getElementById('competitionName').innerHTML;
    window.location.href = competitionName + "/judges";
}

function onStudentScoresClick() {
    competitionName = document.getElementById('competitionName').innerHTML;
    window.location.href = competitionName + "/scores";
}

function onJudgingPageClick() {
    competitionName = document.getElementById('competitionName').innerHTML;
    window.location.href = competitionName + "/judging";
}

function onAddStudentClick() {
    competitionName = document.getElementById('competitionName').innerHTML;
    window.location.href = competitionName + "/students";
}

function onAddCriteriaClick() {
    competitionName = document.getElementById('competitionName').innerHTML;
    window.location.href = competitionName + "/criteria";
}
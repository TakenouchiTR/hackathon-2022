function getLastItem(path) {
    path.substring(path.lastIndexOf('/') + 1)
}

function onEditJudgeClick(appName) {
    competitionName = document.getElementById('competitionName').innerHTML;
    window.location.href = competitionName + "/judges";
}
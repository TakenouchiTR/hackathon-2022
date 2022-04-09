function onStudentScoresClick(appName) {
    competitionName = document.getElementById('competitionName').innerHTML;
    window.location.href = competitionName + "/students";
}
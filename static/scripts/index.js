function onSelectClick() {
    console.log("onSelectClick");
    competitionSelect = document.getElementById("competition_names");
    console.log(competitionSelect.value);
    window.location.href = "app/" + competitionSelect.value;
    
}

/*fetch("api/competition?name=" + competitionSelect.value)
        .then(response => response.json())
        .then(data => console.log(data));*/
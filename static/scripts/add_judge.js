function addJudgePressed() {
    let firstName = document.getElementById("fname").value;
    let lastName = document.getElementById("lname").value;
    let name = firstName + " " + lastName;
    let competitionName = document.getElementById("competitionName").innerHTML;
    let data = {name: competitionName, judge_name: name}

    fetch("../../../api/competition/judge/",{
        method: 'PUT',
        headers:{
        'Content-Type':'application/json'
        },
        body: JSON.stringify({name: competitionName, judge_name: name})
    }).then(response => response.json(data))
        .then(data => console.log(data));
}
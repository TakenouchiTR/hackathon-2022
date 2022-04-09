function addJudgePressed() {
    let firstName = document.getElementById("fname").value;
    let lastName = document.getElementById("lname").value;
    let name = firstName + " " + lastName;
    let competitionName = document.getElementById("competitionName").innerHTML;
    let body = {name: competitionName, judge_name: name}

    fetch("../../../api/competition/student/",{
        method: 'PUT',
        headers:{
        'Content-Type':'application/json'
        },
        body: JSON.stringify({name: competitionName, judge_name: name})
    })
    .then(response => response.json(body))
    .then(data => {
        console.log(data);
        if (data.success_code === 0)
        {
            let li = document.createElement("li");
            li.innerHTML = name;
            let judgeList = document.getElementById("student_names");
            judgeList.appendChild(li);
        }
    });
}
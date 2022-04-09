function addCriteriaPressed() {
    let criteria = document.getElementById("fname").value;
    let competitionName = document.getElementById("competitionName").innerHTML;
    let body = {name: competitionName, criteria: criteria};

    fetch("../../../api/competition/criteria/",{
        method: 'POST',
        headers:{
        'Content-Type':'application/json'
        },
        body: JSON.stringify({name: competitionName, criteria: criteria})
    })
    .then(response => response.json(body))
    .then(data => {
        console.log(data);
        if (data.success_code === 0)
        {
            let li = document.createElement("li");
            li.innerHTML = criteria;
            let judgeList = document.getElementById("criteria_names");
            judgeList.appendChild(li);
        }
    });
}
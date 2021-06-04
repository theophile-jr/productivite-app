taskList = [];

function onTaskAdded() {
    //DESCRIPTION : this function is called after an element was added, It push it to the task array
    //Parameters : None

    taskList.push({
        name: document.getElementById("task").value,
        date: document.getElementById("date").value,
        priority: document.getElementById("priority").value
    });
    console.log(taskList)

    updateTask ();
}

function updateTask () {
    //DESCRIPTION : Add the elements added previousely in the DOM
    //Parameters : None

    console.log(taskList[0].name)
    //Create elements
    for (i=0; i < taskList.length; i++) {
        //Check if the element already exists
        if (!document.getElementById(taskList[i].name + "Task" + i)) {
            var tr = document.createElement("tr");
            tr.setAttribute("id", taskList[i].name + "Task" + i);
            document.getElementById("todo-table").appendChild(tr);

            //Add the name and the checkbox
            var td = document.createElement("td");
            td.innerHTML = "<input type=\"checkbox\"> " + taskList[i].name;
            document.getElementById(taskList[i].name + "Task" + i).appendChild(td);

            //Add the date
            var td = document.createElement("td");
            td.innerHTML = taskList[i].date;
            document.getElementById(taskList[i].name + "Task" + i).appendChild(td);

            //Add the priority
            var td = document.createElement("td");
            td.innerHTML = taskList[i].priority;
            document.getElementById(taskList[i].name + "Task" + i).appendChild(td);
        }
    }
}

function sendTodoForm() {
    //DESCRIPTION : Send data of to the backend
    //Parameters : None
    $.ajax({
        type: "POST",
        url: "/",
        // timeout: 5000,
        data: JSON.stringify({ task: $("#task").val(), date: $("#date").val(), priority: $("#priority").val()}),
        cache: false,
        success: function (success) {
            console.log(success)
        },
        error: function () {
            console.log("Une erreur");
        }
    });
}


window.onload = function GetTodoData() {
    //DESCRIPTION : Send data of to the backend
    //Parameters : None
    $.ajax({
        type: "POST",
        url: "/getdata",
        // timeout: 5000,
        data: JSON.stringify({ }),
        cache: false,
        success: function (todoData) {
            console.log(todoData[1])
            for (y=0; y<todoData.length; y++) {
                console.log(y)
                taskList.push({
                    name: todoData[y][1],
                    date: todoData[y][2],
                    priority: todoData[y][3]
                });
                console.log(taskList)

                updateTask ();
            }
        },
        error: function () {
            console.log("Une erreur");
        }
    });
}

// function clearForm(idForm) {
//     document.getElementById(idForm).reset();
// }
//
// function checkForm(data = []) {
//     for (i = 0; i < data.length; i++) {
//         if (($(data[i]).val()).length <= 0)
//             return false
//     }
//     return true
// }

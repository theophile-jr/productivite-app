taskList = []; //Store user tasks

function createTask() {
    //DESCRIPTION : Add the task in the DOM
    //Parameters : None
    //Return None

    //Create elements
    for (i = 0; i < taskList.length; i++) {

        //Remove the space for the task name
        taskNameWithoutSpace = taskList[i].name.replace(/\s/g, '');

        //Check if the element already exists
        if (!document.getElementById(taskList[i].name + "Task" + i)) {
            //Create a line in the table
            var tr = document.createElement("tr");
            tr.setAttribute("id", taskList[i].name + "Task" + i);
            document.getElementById("todo-table").appendChild(tr);

            //Add the name and the checkbox
            var td = document.createElement("td");
            // console.log(taskList[i].status)
            td.innerHTML = "<input type=\"checkbox\" id=\"" + taskNameWithoutSpace + i + "CheckBox" + "\" onchange=\"taskStatusChanged(this.id); sendTodoForm('updateTaskStatus', '" + taskList[i].taskID + "', this.checked)\" > " + taskList[i].name;
            document.getElementById(taskList[i].name + "Task" + i).appendChild(td);
            if (taskList[i].status == "disable") { //If the task is 'done' mark the checkbox as  checked
                document.getElementById("" + taskNameWithoutSpace + i + "CheckBox" + "").checked = true;
                taskStatusChanged("" + taskNameWithoutSpace + i + "CheckBox" + "") //Add class
            }

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

function sendTodoForm(goal, checkBoxID, checkBoxStatus) {
    //Description : Send the new element created and inform the server when elements have been change
    //Parameters  : goal -> which type of request (updateTaskStatus, addNewElement)
    //              checkBoxID (Only for updateTaskStatus goal) -> The ID of the checkbox to identify the task in the DB
    //              checkBoxStatus (Only for updateTaskStatus goal) -> The status of the checkbox (checked or not)
    //Return      : None

    //Prepare the data to send according to the selected goal
    if (goal == "updateTaskStatus") //Inform the server that a task have been mark as done and vice versa
        data = JSON.stringify({
            goal: 'updateStatus',
            taskID: "" + checkBoxID + "",
            status: !checkBoxStatus ? 'enable' : 'disable'
        })
    else //Creation of new task
        data = JSON.stringify({
            goal: 'addElement',
            task: $("#task").val(),
            date: $("#date").val(),
            priority: $("#priority").val()
        })

    //Send the data
    $.ajax({
        type: "POST",
        url: "/",
        data: data,
        cache: false,
        success: function (success) {
            console.log("Success " + success)
            if (goal != "updateTaskStatus") { //If it's a creation of new task push it to the list
                taskList.push({
                    name: document.getElementById("task").value,
                    date: document.getElementById("date").value,
                    priority: document.getElementById("priority").value,
                    taskID: success //Get the id of the task in the DB
                });
                createTask(); // Show the task in the DOM
            }
        },
        error: function () {
            console.log("An error occurred while sending data");
        }
    });
}

window.onload = function GetTodoData() {
    //DESCRIPTION : Get the user tasks from the DB
    //Parameters : None

    taskList = [];
    $.ajax({
        type: "POST",
        url: "/getdata",
        data: JSON.stringify({}),
        cache: false,
        success: function (todoData) {
            for (y = 0; y < todoData.length; y++) {
                taskList.push({
                    taskID: todoData[y][0],
                    name: todoData[y][2],
                    date: todoData[y][3],
                    priority: todoData[y][4],
                    status: todoData[y][5]
                });
                createTask(); //Show them in the DOM
            }
        },
        error: function () {
            console.log("Une erreur");
        }
    });
}

function taskStatusChanged(checkBoxID) {
    //Description : Apply a style when a task is 'done'.
    //Parameters  : checkBoxID -> The ID of the checkbox
    //Return      : None

    if (document.getElementById(checkBoxID).checked)
        //Add the class to his grandfather
        $("#" + checkBoxID).parentsUntil("table").addClass("line-through")
    else
        $("#" + checkBoxID).parentsUntil("table").removeClass("line-through")
}


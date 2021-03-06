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
        if (!document.getElementById("Task" + taskList[i].taskID)) {
            //Create a line in the table
            var tr = document.createElement("tr");
            tr.setAttribute("id", "Task" + taskList[i].taskID);
            document.getElementById("tasksContent").appendChild(tr);

            //Add the name and the checkbox
            var td = document.createElement("td");
            // console.log(taskList[i].status)
            td.innerHTML = "<input type=\"checkbox\" id=\"" + taskList[i].taskID + i + "CheckBox" + "\" onchange=\"taskStatusChanged(this.id); sendTodoForm('updateTaskStatus', '" + taskList[i].taskID + "', this.checked)\" > " + taskList[i].name;
            document.getElementById("Task" + taskList[i].taskID).appendChild(td);
            if (taskList[i].status == "disable") { //If the task is 'done' mark the checkbox as  checked
                document.getElementById("" + taskList[i].taskID + i + "CheckBox" + "").checked = true;
                taskStatusChanged("" + taskList[i].taskID + i + "CheckBox" + "") //Add class
            }

            //Add the date
            var td = document.createElement("td");
            td.innerHTML = taskList[i].date;
            document.getElementById("Task" + taskList[i].taskID).appendChild(td);

            //Add the priority
            var td = document.createElement("td");
            td.innerHTML = taskList[i].priority;
            document.getElementById("Task" + taskList[i].taskID).appendChild(td);
            
            //Add the tag
            var td = document.createElement("td");
            td.innerHTML = taskList[i].tag;
            document.getElementById("Task" + taskList[i].taskID).appendChild(td);

            //Empty column
            var td = document.createElement("td");
            document.getElementById("Task" + taskList[i].taskID).appendChild(td);

            //Add the trash
            var td = document.createElement("td");
            td.innerHTML = "<button onclick=\"sendTodoForm('removeElement', this.name)\" name='" + taskList[i].taskID + "' class='no-style' ><i class=\"fa fa-trash-o trashbin\" style=\"font-size:20px\"></i></button>"
            document.getElementById("Task" + taskList[i].taskID).appendChild(td);
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
    else if (goal == "removeElement")
        data = JSON.stringify({
            goal: 'removeElement',
            taskID: "" + checkBoxID + ""
        })
    else {
        data = JSON.stringify({
            goal: 'addElement',
            task: $("#task").val(),
            date: $("#date").val(),
            priority: $("#priority").val(),
            tag: $("#tag-selector").val()
        })
        if (!checkTaskForm(data))
            return
    }
    console.log(data)
    //Send the data
    $.ajax({
        type: "POST",
        url: "/",
        data: data,
        cache: false,
        success: function (success) {
            console.log("Success " + success)
            if (goal == "addElement") { //If it's a creation of new task push it to the list
                taskList.push({
                    name: document.getElementById("task").value,
                    date: document.getElementById("date").value,
                    priority: document.getElementById("priority").value,
                    tag: document.getElementById("tag-selector").value,
                    taskID: success //Get the id of the task in the DB
                });
                createTask(); // Update tasks in the DOM
            }
            if (goal == "removeElement") { //If it's a creation of new task push it to the list
                for (z = 0; z < taskList.length; z++) {
                    if (taskList[z].taskID == checkBoxID) {
                        console.log(taskList)
                        taskList.splice(z, z + 1);
                        console.log(taskList)
                        console.log("#" + checkBoxID)
                        $("#Task" + checkBoxID).remove();
                    }
                }
                createTask(); // Update tasks in the DOM
            }
        },
        error: function () {
            console.log("An error occurred while sending data");
        }
    });
}

$(document).ready(function() {
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
                    status: todoData[y][5],
                    tag: todoData[y][6]
                });
                createTask(); //Show them in the DOM
            }
            document.getElementById("tag-selector").addEventListener('focus', function(){
                getTags(this);
            })
        },
        error: function () {
            console.log("An error occurred");
        }
    });
})

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

function checkTaskForm(data) {
    //Description : Check if all input is correct
    //Parameters  : data : -> the data to check
    //Return      : true or false

    data = JSON.parse(data)
    if (data['task'].length <= 0) {
        document.getElementById("taskFormError").innerHTML = "<strong>The task input can't be empty</strong>";
        return false
    } else {
        document.getElementById("taskFormError").innerHTML = "";
        return true
    }
}

function getTags(input) {
    //DESCRIPTION : Get the user tags from the DB
    //Parameters : None

    taskList = [];
    $.ajax({
        type: "POST",
        url: "/gettags",
        data: JSON.stringify({}),
        cache: false,
        success: function (todoTags) {
            tagList= [] 
            todoTags.forEach(tag => {
                if (tag[0]) tagList.push({label :tag[0], value:tag[0]}) 
            });
            $("#tag-selector").autocomplete({source: tagList})
        },
        error: function () {
            console.log("An error occurred");
        }
    });
}

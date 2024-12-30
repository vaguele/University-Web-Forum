
const loaded = document.getElementById('login');
if (loaded){
    document.getElementById("login").addEventListener("submit", function (event) {
        event.preventDefault()

        console.log("Login/Register Buttons")
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;
        var activeElement = document.activeElement;

        string = 'https://ucmsocialmediaapp.pythonanywhere.com/login';

        if (username.includes("<") || username.includes("/") || username.includes(">") || username.includes("'") || username.includes("&") || password.includes("<") || password.includes("/") || password.includes(">") || password.includes("'") || password.includes("&")){
            window.alert("Don't use special characters (<,>,/,',&).")
        }
        else if (username == "" && password == ""){
            window.alert("Please Enter a Username and Password.")
        }
        else if (username == "" && password != ""){
            window.alert("Please Enter a Username.")
        }
        else if (username != "" && password == ""){
            window.alert("Please Enter a Password.")
        }
        else if (activeElement.value == "reg") {
            console.log("reg")
            var request = new XMLHttpRequest();
            request.open('POST', string);
            request.setRequestHeader("Content-Type", "application/json");
            request.onload = function () {
                console.log(request.responseText)
                window.alert(request.responseText)
            }
            const body = { "username": username, "password": password };
            console.log(body)
            request.send(JSON.stringify(body));


        }
        else {
            var request = new XMLHttpRequest();
            string += "/" + username + "/" + password
            console.log(string)
            request.open('GET', string);
            request.setRequestHeader("Content-Type", "application/json");
            request.onload = function () {
                //window.alert(request.responseText)
                console.log("RAN")
                if (request.responseText != "incorrect password or username"){


                    place =  "https://ucmsocialmediaapp.pythonanywhere.com/mainpage/" + request.responseText
                    if (request.responseText == "admin"){
                        place = "https://ucmsocialmediaapp.pythonanywhere.com/admin"
                    }
                    window.location.href = place
                }
            }
            request.send();

        }
    });
}
// function postwork(){
//     document.getElementById('createElementsBtn').addEventListener('click', function() {
//         var textBox = document.createElement('input');
//         textBox.type = 'text';
//         textBox.placeholder = 'Enter text';

//         var newButton = document.createElement('button');
//         newButton.textContent = 'Submit Post';

//         var container = document.querySelector('.container');
//         container.appendChild(textBox);
//         container.appendChild(newButton);
//     });
// }

const loaded2 = document.getElementById('PostDashboard');
console.log(loaded2)
if (loaded2) {
    document.getElementById("postToDashboard").addEventListener("submit", function (event) {
        event.preventDefault();
        console.log("buttonClicked");
        let yourPost = document.getElementById("yourPost").value;
        let username = document.getElementById("PostDashboard").value;

        if (yourPost.includes("<") || yourPost.includes("/") || yourPost.includes(">") || yourPost.includes("'") || yourPost.includes("&")) {
            window.alert("Don't use special characters (<,>,/,',&)")
        } else {
            console.log("postToDashboardRan");
            var request = new XMLHttpRequest();
            string = "https://ucmsocialmediaapp.pythonanywhere.com/post";
            request.open('POST', string);
            request.setRequestHeader("Content-Type", "application/json");
            request.onload = function () {
                console.log(request.responseText);

            };
            const body = { "username": username, "body": yourPost, "replyTo" : 0, "tag": "mainpage"};
            console.log(body);
            request.send(JSON.stringify(body));

        }
    });
}

const loaded3 = document.getElementById('PostDashboard');
if (loaded3){
    setInterval(showPosts, 10000); //10 seconds

    function showPosts() {
        let username = document.getElementById("PostDashboard").value;
        console.log(username)
        var request = new XMLHttpRequest();
        string = "https://ucmsocialmediaapp.pythonanywhere.com/post/" + username + "/mainpage";
        request.open('GET', string);
        request.onload = function () {
            //console.log(request.responseText);
            displayRawData(request.responseText)
        };
        request.send();

    }
}

/*
function displayRawData(responseText) {
    var postsTable = document.getElementById("postsTable");

    var newRow = postsTable.insertRow();
    var newCell = newRow.insertCell();
    var preElement = document.createElement("pre");
    preElement.textContent = responseText;
    newCell.appendChild(preElement);
}
*/

function displayRawData(responseText) {
  // Parse the JSON response
  var posts = JSON.parse(responseText);

  // Get the container where you want to append the posts
  var container = document.getElementById("postContainer");
  container.className = "scroll-container";
  // Clear the container before appending new posts
  container.innerHTML = "";

  // Iterate over each post in the response
  posts.forEach(function(post) {
    // Create elements for post details
    var postElement = document.createElement("div");
    postElement.className = "post";

    var userId = document.createElement("p");
    userId.textContent = "User ID: " + post.userId + "Username:" + post.Username;



    var postBody = document.createElement("p");
    postBody.textContent = "Post Body: " + post.Post_Body;

    var timePosted = document.createElement("p");
    timePosted.textContent = "Time Posted: " + post.time_posted;

    var rating = document.createElement("p");
    rating.textContent = "Rating: " + post.rating;

    // Append post details to the post element
    postElement.appendChild(userId);
    postElement.appendChild(postBody);
    postElement.appendChild(timePosted);
    postElement.appendChild(rating);

    var upvote = document.createElement("button")
    upvote.textContent = "⇧"
    upvote.classList.add("up")
    upvote.value = post.postID

    var downvote = document.createElement("button")
    downvote.textContent = "⇩"
    downvote.classList.add("down")
    downvote.value = post.postID
    /*
    var inp = document.createElement("input")
    inp.setAttribute("type", "text");
    inp.setAttribute("id", "yourPost");
    inp.setAttribute("name", "yourPost");
    inp.setAttribute("autocomplete", "on");
    inp.setAttribute("placeholder", "Enter Your Response Text");
    inp.classList.add("inputter")

    var reply = document.createElement("button")
    reply.setAttribute("type", "submit");
    reply.setAttribute("id", "PostDashboard");
    reply.setAttribute("value", "{{username}}");
    reply.textContent = "Reply"
    reply.classList.add("reply")
    reply.value = post.postID
    */
    postElement.appendChild(upvote);
    postElement.appendChild(downvote);
    //postElement.appendChild(inp);
    //postElement.appendChild(reply);

    // Append post element to the container
    container.appendChild(postElement);
  });
}


/*

function fetchAndDisplayPostsData() {
    // Simulate an asynchronous request to fetch the posts data
    fetch("/mainpage/addpost/<username>") // Replace with the appropriate URL for fetching the posts
        .then(function(response) {
            return response.text();
        })
        .then(function(responseText) {
            // Call the displayRawData function with the response
            displayRawData(responseText);
        })
        .catch(function(error) {
            console.log("Error:", error);
        });
}

// Call the function when the page loads
window.onload = function() {
    fetchAndDisplayPostsData();
};



// Iterate over each post in the response

posts.forEach(function(post) {
  // Create elements for post details
  var postElement = document.createElement("div");
  postElement.className = "post";

  var userId = document.createElement("p");
  userId.textContent = "User ID: " + post.userId;

  var postBody = document.createElement("p");
  postBody.textContent = "Post Body: " + post.Post_Body;

  var timePosted = document.createElement("p");
  timePosted.textContent = "Time Posted: " + post.time_posted;

  var rating = document.createElement("p");
  rating.textContent = "Rating: " + post.rating;

  // Append post details to the post element
  postElement.appendChild(userId);
  postElement.appendChild(postBody);
  postElement.appendChild(timePosted);
  postElement.appendChild(rating);

  // Create buttons for liking and disliking
  var upvote = document.createElement("button")
  upvote.textContent = "⇧"
  upvote.classList.add("up")
  upvote.value = post.postID


  var downvote = document.createElement("button")
  downvote.textContent = "⇩"
  downvote.classList.add("down")
  downvote.value = post.postID


  // Append buttons to the post element
  postElement.appendChild(upvote);
  postElement.appendChild(downvote);

  // Append post element to the container
  container.appendChild(postElement);
});

*/


function like(attraction, username){
    var request = new XMLHttpRequest();
    string = "https://ucmsocialmediaapp.pythonanywhere.com/like/" + attraction;
    request.open('PUT', string);
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = function () {
        window.alert(request.responseText);
        //displayRawData(request.responseText);
    };
    const body = {"likeOrDislike": 1, "username": username};
    console.log(body);
    request.send(JSON.stringify(body));
    displayLikes(attraction)
}

function dislike(attraction, username){
    var request = new XMLHttpRequest();
    string = "https://ucmsocialmediaapp.pythonanywhere.com/like/" + attraction;
    request.open('PUT', string);
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = function () {
        window.alert(request.responseText);
        //displayRawData(request.responseText);
    };
    const body = {"likeOrDislike": -1, "username": username};
    console.log(body);
    request.send(JSON.stringify(body));
    displayLikes(attraction)
}

function displayLikes(attraction){
    var request = new XMLHttpRequest();
    string = "https://ucmsocialmediaapp.pythonanywhere.com/like/" + attraction;
    request.open('GET', string);
    request.setRequestHeader("Content-Type", "application/json");
    request.onload = function () {
        likes = JSON.parse(request.responseText)
        document.getElementById(attraction).value = likes[0]['likes'];
    };
    request.send();
}





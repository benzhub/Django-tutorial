const form = document.getElementById("login-form")

form.addEventListener("submit", (e) => {
    e.preventDefault()
    // console.log("Form was Submitted!")
    let formData = {
        "username": form.username.value,
        "password": form.password.value
    }

    // console.log(formData)
    fetch(`http://127.0.0.1:8000/api/users/token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      })
        .then(response => response.json())
        .then(result => {
        //   console.log(result)
        if (result.access) {
            localStorage.setItem("token", result.access)
        } else {
            alert("Username OR Password did not work")
        }
        })
        .then((data) => {
            window.location = "http://127.0.0.1:5500/projects-list.html"
        })
        .catch(error => console.log('error', error));
})
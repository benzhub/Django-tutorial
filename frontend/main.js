// console.log("I love Javascript!")

let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token')

if (token) {
  loginBtn.remove()
} else {
  logoutBtn.remove()
}

logoutBtn.addEventListener("click", (e) => {
  e.preventDefault()
  localStorage.removeItem("token")
  window.location = "http://127.0.0.1:5500/login.html"
})

const baseUrl = "http://127.0.0.1:8000"
const projectsUrl = `${baseUrl}/api/projects/`


const getProjects = () => {
  fetch(projectsUrl)
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      buildProjects(data)
    })
};

const buildProjects = (projects) => {
  let projectsWrapper = document.getElementById("projects-wrapper")
  projectsWrapper.innerHTML = ''
  for (let project of projects) {
    // console.log(project)
    projectsWrapper.innerHTML += `
      <div class="project--card">
        <img src="${baseUrl}${project.featured_image}"/>

        <div>
          <div>
            <div class="card--header">
              <h3>${project.title}</h3>
              <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
              <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
            </div>
            <i>${project.vote_ratio}% Positive feedback</i>
            <p>${project.description.substring(0, 150)}</p>
          </div>
        </div>
      </div>
    `
    addVoteEvents()
  }

  // add a listener

}

const addVoteEvents = () => {
  let voteBtns = document.getElementsByClassName("vote--option")
  // console.log(`voteBtns: ${voteBtns}`)
  for (let i=0; i < voteBtns.length; i++) {
    voteBtns[i].addEventListener("click", (e) => {
      // console.log(token)
      // console.log("Vote was clicked:", i)
      let vote = e.target.dataset.vote
      let project = e.target.dataset.project
      // console.log(`project: ${project}, vote: ${vote}`)

      fetch(`http://127.0.0.1:8000/api/projects/${project}/vote`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({"value": vote})
      })
        .then(response => response.json())
        .then(result => {
          console.log(result)
          getProjects()
        })
        .catch(error => console.log('error', error));
    })
  }
}

getProjects()
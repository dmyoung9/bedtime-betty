const spinner = document.getElementById('spinner');
const themesContainer = document.getElementById('themesContainer');
const lessonsContainer = document.getElementById('lessonsContainer');
const buttons = document.getElementById('buttons');
const refreshButton = document.getElementById('refreshButton');

const themesWs = `ws://192.168.1.212:5000/api/stories/themes/stream`;
const lessonsWs = `ws://192.168.1.212:5000/api/stories/lessons/stream`;

let apiKey;
let minAge;
let maxAge;

let story_id;
let current_theme;
let current_story;
let current_lesson;

let socket;
let headers;

var isLoading = false;
var isThemeButtonSelected = false;
var isLessonButtonSelected = false;

const containerIds = ['themesContainer', 'lessonsContainer'];
let currentContainerIndex = 0;

// Add theme button to the DOM
function addButton(theme) {
  const col = createColumnElement();
  const button = createThemeButton(theme);
  col.appendChild(button);
  themesContainer.appendChild(col);
  animateButton(button);
}

// Add theme button to the DOM
function addLesson(lesson) {
  const col = createColumnElement();
  const button = createLessonButton(lesson);
  col.appendChild(button);
  lessonsContainer.appendChild(col);
  animateButton(button);
}

function createColumnElement() {
  const col = document.createElement('div');
  col.classList.add('col-12', 'col-md-4', 'mb-2', 'justify-content-center');
  return col;
}

function createThemeButton(theme) {
  const button = document.createElement('button');
  button.innerHTML = `${theme.emoji}<br>${theme.story_theme}`;
  button.style.backgroundColor = `${theme.color}`;
  button.style.color = `${theme.text_color}`;
  button.style.border = 'none';
  button.classList.add('btn', 'btn-primary', 'mr-2', 'mb-2', 'w-100', 'h-100', 'theme-btn');

  button.addEventListener("click", async () => {
    chooseTheme(theme);
    fetchFromWebSocket(lessonsWs, 9);
  });

  return button;
}

function createLessonButton(lesson) {
  const button = document.createElement('button');
  button.innerHTML = `${lesson}`;
  button.style.backgroundColor = `${current_theme.color}`;
  button.style.color = `${current_theme.text_color}`;
  button.style.border = 'none';
  button.classList.add('btn', 'btn-primary', 'mr-2', 'mb-2', 'w-100', 'h-100', 'theme-btn');

  button.addEventListener("click", () => {
    current_lesson = lesson;
  });

  return button;
}

async function updateTheme(theme) {
  var body = JSON.stringify(theme);

  var requestOptions = {
    method: 'PATCH',
    headers: headers,
    body: body,
    redirect: 'follow'
  };

  await fetch(`http://192.168.1.212:5000/api/stories/${story_id}/theme`, requestOptions)
    .then(response => response.json())
    .then(result => current_story = result)
    .catch(error => console.log('error', error));
}

async function updateLesson(lesson) {
  var body = JSON.stringify({ story_lesson: lesson });

  var requestOptions = {
    method: 'PATCH',
    headers: headers,
    body: body,
    redirect: 'follow'
  };

  await fetch(`http://192.168.1.212:5000/api/stories/${story_id}/lesson`, requestOptions)
    .then(response => response.json())
    .then(result => current_story = result)
    .catch(error => console.log('error', error));
}

function animateButton(button) {
  setTimeout(() => {
    button.classList.add("loaded");
  }, 100);
}

// Spinner control functions
function showSpinner() {
  spinner.style.display = 'block';
  buttons.style.display = 'none';
}

function hideSpinner() {
  spinner.style.display = 'none';
  buttons.style.display = 'block';
  isLoading = false;
}

// Main function
document.addEventListener('DOMContentLoaded', async function () {
  apiKey = localStorage.getItem('apiKey') || '';
  minAge = localStorage.getItem('minAge') || '';
  maxAge = localStorage.getItem('maxAge') || '';

  headers = new Headers();
  headers.append("OPENAI_API_KEY", apiKey);
  headers.append("Content-Type", "application/json");

  if (!apiKey) {
    alert('Please enter your API key on the settings page.');
    return;
  }

  refreshButton.addEventListener("click", async function () {
    const currentContainer = document.getElementById(containerIds[currentContainerIndex]);

    switch (currentContainer.id) {
      case 'themesContainer':
        fetchFromWebSocket(themesWs, 3);
        break;
      case 'lessonsContainer':
        fetchFromWebSocket(lessonsWs, 3);
        break;
      default:
        console.error('Invalid container ID');
    }
  });

  await fetchFromWebSocket(themesWs, 3);
});

async function startStory(minAge, maxAge) {
  const body = {
    "age_min": minAge,
    "age_max": maxAge
  };

  var requestOptions = {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(body),
    redirect: 'follow'
  };

  let story_id;

  await fetch("http://127.0.0.1:5000/api/stories/start", requestOptions)
    .then(response => response.json())
    .then(data => story_id = data.story)
    .catch(error => console.log('error', error));

  return story_id;
}

async function chooseTheme(theme) {
  current_theme = theme;
  story_id = await startStory(minAge, maxAge);
  await updateTheme(theme);

  themesContainer.classList.add("slide-left");
  lessonsContainer.classList.remove("slide-right");
  currentContainerIndex++;
}

async function chooseLesson(lesson) {
  current_lesson = lesson;
  await updateLesson(lesson);
}

function getSocket(url, num) {
  let socket = new WebSocket(url);

  socket.addEventListener("open", () => {
    console.log("WebSocket connection opened.");
    showSpinner();
    isLoading = true;
    const body = { type: "request", data: { api_key: apiKey, age_min: minAge, age_max: maxAge, num: num } };
    socket.send(JSON.stringify(body));
  });

  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    console.log(data)

    if (data.type === "end") {
      hideSpinner();
    } else if (data.type === "theme") {
      addButton(data.theme);
    } else if (data.type === "lesson") {
      addLesson(data.lesson);
    }
  });

  socket.addEventListener("close", () => {
    if (isLoading) {
      hideSpinner();
    }

    console.log("WebSocket connection closed.");
  });

  return socket;
}

async function safe_close_socket() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    await socket.close();
  }
}

// Fetch themes via WebSocket
async function fetchFromWebSocket(url, num) {
  await safe_close_socket();
  socket = getSocket(url, num);
}
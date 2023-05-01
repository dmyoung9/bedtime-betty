const spinner = document.getElementById('spinner');
const themesContainer = document.getElementById('themesContainer');
const buttons = document.getElementById('buttons');
const refreshButton = document.getElementById('refreshButton');
const goButton = document.getElementById('goButton');

const themesWs = `ws://192.168.1.212:5000/api/stories/themes/stream`;

let apiKey;
let minAge;
let maxAge;

let story_id;
let current_story;

let socket;
let headers;

// Add theme button to the DOM
function addButton(theme) {
  const col = createColumnElement();
  const button = createThemeButton(theme);
  col.appendChild(button);
  themesContainer.appendChild(col);
  animateButton(button);
}

function createColumnElement() {
  const col = document.createElement('div');
  col.classList.add('col-12', 'col-md-4', 'mb-2', 'd-flex', 'justify-content-center');
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
    var body = JSON.stringify(theme);

    var requestOptions = {
      method: 'PATCH',
      headers: headers,
      body: body,
      redirect: 'follow'
    };

    fetch(`http://192.168.1.212:5000/api/stories/${story_id}/theme`, requestOptions)
      .then(response => response.text())
      .then(result => current_story = result)
      .catch(error => console.log('error', error));
  });

  return button;
}

function animateButton(button) {
  setTimeout(() => {
    button.classList.add("loaded");
  }, 100);
}

// Establish a WebSocket connection
function getSocket(url, num) {
  let socket = new WebSocket(url);

  socket.addEventListener("open", () => {
    const body = { type: "request", data: { api_key: apiKey, age_min: minAge, age_max: maxAge, num: num } };
    socket.send(JSON.stringify(body));
  });

  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "end") {
      console.log("Generator finished.");
      hideSpinner();
      return;
    } else if (data.type === "theme") {
      addButton(data.theme);
    }
  });

  socket.addEventListener("close", () => {
    console.log("WebSocket connection closed.");
  });

  return socket;
}

// Spinner control functions
function showSpinner() {
  spinner.style.display = 'block';
  buttons.style.display = 'none';
}

function hideSpinner() {
  spinner.style.display = 'none';
  buttons.style.display = 'block';
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

  story_id = await startStory(minAge, maxAge);

  refreshButton.addEventListener("click", function () {
    fetchFromWebSocket(themesWs, 3);
  });

  goButton.addEventListener("click", function () {
    chooseLesson(story_id);
  });

  setupThemeButtonListeners();
  fetchFromWebSocket(themesWs, 5);
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

async function chooseLesson(story_id) {

}

// Fetch themes via WebSocket
function fetchFromWebSocket(url, num) {
  showSpinner();

  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close();
  }

  socket = getSocket(url, num);
}

function setupThemeButtonListeners() {
  themesContainer.addEventListener('focus', function (event) {
    if (event.target.tagName === 'BUTTON') {
      goButton.disabled = false;
    }
  }, true); // Use event capturing

  themesContainer.addEventListener('blur', function (event) {
    if (event.target.tagName === 'BUTTON') {
      goButton.disabled = true;
    }
  }, true); // Use event capturing
}
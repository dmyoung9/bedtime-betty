const themesRow = document.getElementById("themesRow");
const loadingSpinner = document.getElementById("loadingSpinner");
const loadingSpinnerLabel = document.getElementById("loadingSpinnerLabel");
const readButton = document.getElementById("readButton");
const nextButton = document.getElementById("nextButton");
const nextSpinner = document.getElementById("nextSpinner");

var sockets = {};
var chosenTheme = null;
var chosenLesson = null;
var chosenAuthor = null;
var chosenArtist = null;
var chosenTitle = null;
var paragraphs = [];

const base_api_url = `http://${window.config.BASE_API_URL}`;
const ws_api_url = `ws://${window.config.BASE_API_URL}`;
const totalParagraphs = 7;

function showSpinner(element, labelElement = null, label = null) {
    console.log(label);
    const spinner = document.getElementById(element);

    if (label) {
        const text = document.getElementById(labelElement);
        text.innerHTML = label;
    }

    // console.log(loadingSpinner.classList);
    if (spinner.classList.contains('invisible')) {
        spinner.classList.remove('invisible');
    }
    // console.log(loadingSpinner.classList);
}

function hideSpinner(element) {
    console.log("hiding spinner");
    let spinner = document.getElementById(element);

    // console.log(loadingSpinner.classList);
    if (!spinner.classList.contains('invisible')) {
        spinner.classList.add('invisible');
    }
    // console.log(loadingSpinner.classList);
}

async function addOption(option, formatFunc, actionFunc, end = false) {
    const optionCol = document.createElement('div');
    optionCol.classList.add('col-12', 'mb-3');

    let optionElement = document.createElement('button');
    optionElement.classList.add('btn', 'btn-primary', 'option-btn');

    if (formatFunc) {
        optionElement = await formatFunc(optionElement, option);
    }

    if (actionFunc) {
        optionElement.addEventListener('click', async () => {
            const idx = Array.from(themesRow.children).indexOf(optionCol);
            await actionFunc(option, idx);
        });
    }

    optionCol.appendChild(optionElement);
    if (end) {
        themesRow.appendChild(optionCol)
    } else {
        themesRow.insertBefore(optionCol, themesRow.firstChild);
    }

    setTimeout(() => {
        optionElement.classList.add("loaded")
    }, 100);
}

async function slideOutOptions(chosenIndex) {
    const themesRow = document.getElementById("themesRow");

    const addSlideClass = (element, delay) => {
        return new Promise(resolve => {
            setTimeout(async () => {
                if (element && element.classList) {
                    element.classList.add('invisible');
                    element.firstChild.classList.add('disappear');
                    element.firstChild.classList.remove('loaded');
                    // await setTimeout(() => { element.classList.add('invisible'); }, delay * 2);
                }
            }, delay);
            resolve();
        });
    };

    for (let idx in themesRow.children) {
        if (idx == chosenIndex) {
            continue;
        }
        await addSlideClass(themesRow.children[idx], 200);
    }
}

function formatThemeButton(button, theme) {
    button.innerHTML = `${theme.emoji}<br>${theme.story_theme}`;
    button.style.backgroundColor = `${theme.color}`;
    button.style.color = `${getContrastTextColor(theme.color)}`;
    button.style.fontFamily = `${theme.font}`;

    return button
}

function formatTitleButton(button, title) {
    button.innerHTML = `This story is called:<br>"${title}"`;
    button.style.backgroundColor = `${chosenTheme.color}`;
    button.style.color = `${getContrastTextColor(chosenTheme.color)}`;

    return button
}

function formatLessonButton(button, lesson) {
    button.innerHTML = `it's about '${lesson}'`;
    button.style.backgroundColor = `${chosenTheme.color}`;
    button.style.color = `${getContrastTextColor(chosenTheme.color)}`;
    // button.style.fontFamily = `${chosenTheme.font}`;

    return button
}

function formatAuthorButton(button, author) {
    button.innerHTML = `in the style of ${author.author_name}<br>(${author.author_style})`;
    button.style.backgroundColor = `${chosenTheme.color}`;
    button.style.color = `${getContrastTextColor(chosenTheme.color)}`;
    // button.style.fontFamily = `${chosenTheme.font}`;

    return button
}

function formatArtistButton(button, artist) {
    button.innerHTML = `with illustrations inspired by ${artist.artist_name}<br>(${artist.artist_style})`;
    button.style.backgroundColor = `${chosenTheme.color}`;
    button.style.color = `${getContrastTextColor(chosenTheme.color)}`;
    // button.style.fontFamily = `${chosenTheme.font}`;

    return button
}

async function formatPage(element, page) {
    let imgSrc = await postToUrl(`${base_api_url}/api/stories/image`, null, requestData = { story_paragraph: page, ...buildStoryInfo() }, json = false);

    const div = document.createElement('div');
    div.classList.add('col-12', 'text-center', 'story-text');

    const img = document.createElement('img');
    img.src = imgSrc;
    img.classList.add('img-fluid', 'rounded', 'mx-auto', 'd-block');

    const text = document.createElement('p');
    text.innerHTML = page;
    text.classList.add('mt-3', 'mb-3', 'bg-body-tertiary', 'rounded', 'p-2');

    div.appendChild(img);
    div.appendChild(text);

    return div
}

function buildRequestData(num) {
    const minAge = localStorage.getItem('minAge') || '';
    const maxAge = localStorage.getItem('maxAge') || '';

    return { age_min: minAge, age_max: maxAge, num: num };
}

function buildStoryInfo(totalParagraphs = 7) {
    const minAge = localStorage.getItem('minAge') || 2;
    const maxAge = localStorage.getItem('maxAge') || 7;

    const storyInfo = { age_min: minAge, age_max: maxAge, story_title: chosenTitle, story_theme: chosenTheme.story_theme, story_lesson: chosenLesson, total_paragraphs: totalParagraphs, previous_paragraphs: paragraphs, ...chosenAuthor, ...chosenArtist };
    return storyInfo;
}

async function fetchOptionsFromWebsocket(url, label, formatFunc = null, actionFunc = null, num = 7, data = null, end = false, spinner = true) {
    const apiKey = localStorage.getItem('apiKey') || '';
    const requestData = data || buildRequestData(num);
    requestData['api_key'] = apiKey;

    return new Promise((resolve, reject) => {
        const socket = new WebSocket(url);

        socket.addEventListener('open', () => {
            console.log('WebSocket connection opened.');
            if (spinner) {
                showSpinner("loadingSpinner", "loadingSpinnerLabel", label);
            }
            var request_msg = { type: 'request', data: requestData }
            socket.send(JSON.stringify(request_msg));
        });

        socket.addEventListener('message', async (event) => {
            const data = JSON.parse(event.data);
            console.log(data)
            if (data.type === 'end') {
                socket.close();
                resolve();
            } else if (data.type === 'item') {
                await addOption(data.data, formatFunc, actionFunc, end);
            }
        });

        socket.addEventListener('close', () => {
            console.log('WebSocket connection closed.');
        });

        socket.addEventListener('error', (error) => {
            console.error('WebSocket error:', error);
            reject(error);
        });

        sockets[label] = socket;
    });
}

async function postToUrl(url, num, requestData = null, json = true) {
    const apiKey = localStorage.getItem('apiKey') || '';
    const headers = new Headers()
    headers.append("Content-Type", "application/json");
    headers.append("Authorization", `Bearer ${apiKey}`);

    const data = requestData || buildRequestData(num)

    var requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data),
        redirect: 'follow'
    };

    const result = await fetch(url, requestOptions)
        .then(response => json ? response.json() : response.text())
        .then(result => {
            console.log(result)
            return result;
        })
        .catch(error => console.log('error', error))

    return result;
}

async function buildStoryDetails(theme, idx) {
    chosenTheme = theme;

    showSpinner("loadingSpinner", "loadingSpinnerLabel", "In a hurry, are we?");
    for (let idx in sockets) {
        await sockets[idx].close();
    }
    await slideOutOptions(-1);

    showSpinner("loadingSpinner", "loadingSpinnerLabel", "Ok, let me think about it...");
    let lessons = await postToUrl(`${base_api_url}/api/stories/lessons`, num = 10);

    const randomLesson = lessons[Math.floor(Math.random() * lessons.length)];
    chosenLesson = randomLesson;
    console.log(randomLesson);

    let titleRequestData = buildRequestData(5);
    titleRequestData['story_theme'] = chosenTheme.story_theme;
    titleRequestData['story_lesson'] = chosenLesson;

    let titles = await postToUrl(`${base_api_url}/api/stories/titles`, num = 5, requestData = titleRequestData);
    const randomTitle = titles[Math.floor(Math.random() * titles.length)];
    chosenTitle = randomTitle;

    showSpinner("loadingSpinner", "loadingSpinnerLabel", "Oh, I've got a good one!");
    addOption(randomTitle, formatTitleButton, null, true);
    addOption(randomLesson, formatLessonButton, null, true);
    console.log(randomTitle);

    let authors = await postToUrl(`${base_api_url}/api/stories/authors`, num = 5);
    const randomAuthor = authors[Math.floor(Math.random() * authors.length)];
    chosenAuthor = randomAuthor;
    showSpinner("loadingSpinner", "loadingSpinnerLabel", "Yep, that should do nicely...");
    addOption(randomAuthor, formatAuthorButton, null, true);
    console.log(randomAuthor);

    showSpinner("loadingSpinner", "loadingSpinnerLabel", "One more thing...");
    let artists = await postToUrl(`${base_api_url}/api/stories/artists`, num = 5);
    const randomArtist = artists[Math.floor(Math.random() * artists.length)];
    chosenArtist = randomArtist;
    addOption(randomArtist, formatArtistButton, null, true);
    console.log(randomArtist);

    setTimeout(() => { hideSpinner("loadingSpinner"); }, 50);

    readButton.classList.add('loaded');
    nextButton.classList.add('loaded');
}

function getContrastTextColor(hexColor) {
    // Check if the input is a valid hex color
    if (!/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hexColor)) {
        throw new Error('Invalid hex color format');
    }

    // Convert 3-digit hex to 6-digit hex
    if (hexColor.length === 4) {
        hexColor = hexColor
            .split('')
            .map((c) => (c !== '#' ? c + c : c))
            .join('');
    }

    // Calculate the brightness of the color
    const r = parseInt(hexColor.substr(1, 2), 16);
    const g = parseInt(hexColor.substr(3, 2), 16);
    const b = parseInt(hexColor.substr(5, 2), 16);
    const brightness = (r * 299 + g * 587 + b * 114) / 1000;

    // Determine if the color is light or dark
    return brightness > 128 ? 'black' : 'white';
}

async function getThemes() {
    nextButton.classList.remove('loaded');
    readButton.classList.remove('loaded');
    await fetchOptionsFromWebsocket(`${ws_api_url}/api/stories/themes/stream`, "Let's come up with some ideas...", formatThemeButton, buildStoryDetails);
}


async function getNextPage() {
    hideSpinner("loadingSpinner");
    // slideOutOptions(-1);

    const storyInfo = buildStoryInfo(totalParagraphs);
    console.log(storyInfo);

    showSpinner("nextSpinner", null);
    readButton.classList.remove('loaded')
    nextButton.classList.remove('loaded')
    await fetchOptionsFromWebsocket(`${ws_api_url}/api/stories/stream`, null, formatPage, null, null, storyInfo, true, false);

    hideSpinner("nextSpinner");
    // nextButton.classList.add('loaded')
    // for (let i = 0; i < totalParagraphs; i++) {

    // }

    // const paragraph = await postToUrl("http://192.168.1.212:5000/api/stories/next", null, storyInfo, false);
    // paragraphs.push(paragraph);
    // addParagraph(paragraph);
}


document.addEventListener('DOMContentLoaded', async () => {
    readButton.addEventListener("click", async () => {
        getNextPage();
    });

    nextButton.addEventListener("click", async () => {
        showSpinner("loadingSpinner", "loadingSpinnerLabel", "In a hurry, are we?");
        for (let idx in sockets) {
            await sockets[idx].close();
        }
        await slideOutOptions(-1);

        chosenTheme = null;
        chosenLesson = null;
        chosenAuthor = null;
        chosenArtist = null;
        chosenTitle = null;
        paragraphs = [];

        getThemes();
    });

    getThemes();
});
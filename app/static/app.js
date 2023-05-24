
import { generate, stream } from './apiClient.js';

let ideas = [];
let lessons = [];
let authors = [];
let artists = [];
let API_KEY;

async function fetchData() {
    const ideas = generate('ideas', { age: 9, num: 7 });
    const lessons = generate('lessons', { age: 9, num: 7 });
    const authors = generate('authors', { age: 9, num: 7 });
    const artists = generate('artists', { age: 9, num: 7 });

    const [initialIdeas,
        initialLessons,
        initialAuthors,
        initialArtists] = await Promise.all([
            ideas,
            lessons,
            authors,
            artists]);
}

function buildStoryFromIdea(age) {
    if (ideas.length && lessons.length && authors.length && artists.length) {
        const idea = ideas.shift();
        const lesson = lessons[Math.floor(Math.random() * lessons.length)];
        const author = authors[Math.floor(Math.random() * authors.length)];
        const artist = artists[Math.floor(Math.random() * artists.length)];

        addStoryCard({ age, idea, lesson, author, artist });

        if (ideas.length) {
            setTimeout(buildStoryFromIdea(age), 500);
        }
    }
}

function addImageToCard(image, card) {
    let img = document.createElement('img');
    img.src = image.url;
    card.appendChild(img);
}

async function addStoryCard(storyDetails) {
    let card = document.createElement('div');
    card.classList.add('card');

    // card.addEventListener('click', function () {
    //     expandCard(card);
    // });

    let emoji = document.createElement('h1');
    emoji.classList.add('card-emoji');
    emoji.innerHTML = storyDetails.idea.emoji;

    let image = document.createElement('div');
    image.classList.add('card-image');

    const storyTitle = await generate(API_KEY, "titles", { age: storyDetails.age, num: 1, story_author: storyDetails.author, story_lesson: storyDetails.lesson, story_idea: storyDetails.idea });
    generate(API_KEY, "images", { num: 1, size: 512, story_artist: storyDetails.artist, story_description: { content: storyTitle } }, data => addImageToCard(data[0], image));

    let title = document.createElement('h1');
    title.classList.add('card-title');
    title.innerHTML = storyTitle[0].title;

    let divider = document.createElement('hr');
    divider.classList.add('solid');

    let cardContent = document.createElement('p');
    cardContent.classList.add('card-content');
    cardContent.innerHTML = `in the style of ${storyDetails.author.author_name}, with illustrations inspired by ${storyDetails.artist.artist_name}`;;

    // for (let key in storyDetails) {
    //     let item = document.createElement('div');
    //     item.classList.add(key);
    //     item.textContent = JSON.stringify(storyDetails[key]);
    //     card.appendChild(item);
    // }

    card.appendChild(emoji);
    card.appendChild(image);
    card.appendChild(title);
    card.appendChild(divider);
    card.appendChild(cardContent);

    const content = document.getElementById("content")
    content.appendChild(card);

    setTimeout(() => { card.classList.add('loaded') }, 100);
}

async function streamData() {
    const age = localStorage.getItem('maxAge') || '';
    // const lesson_request = generate('lessons', request_params);
    // const author_request = generate('authors', request_params);
    // const artist_request = generate('artists', request_params);

    // [lessons, authors, artists] = await Promise.all([lesson_request, author_request, artist_request]);

    stream(API_KEY, 'lessons', { age: age, num: 7 }, data => lessons.push(data));
    stream(API_KEY, 'authors', { age: age, num: 15 }, data => authors.push(data));
    stream(API_KEY, 'artists', { age: age, num: 15 }, data => artists.push(data));
    stream(API_KEY, 'ideas', { age: age, num: 10 }, data => {
        ideas.push(data);
        setTimeout(buildStoryFromIdea(age), 500);
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    API_KEY = localStorage.getItem('apiKey') || '';

    document.querySelector('.overlay').addEventListener('click', function () {
        // Shrink the card and hide the overlay
        document.querySelectorAll('.card.expanded').forEach(card => {
            collapseCard(card);
        });
        this.classList.remove('visible');
    });

    streamData();
});

function expandCard(card) {
    card.dataset.initialWidth = card.offsetWidth;
    card.dataset.initialHeight = card.offsetHeight;
    var rect = card.getBoundingClientRect();
    card.dataset.initialLeft = rect.left + window.scrollX;
    card.dataset.initialTop = rect.top + window.scrollY;

    // Calculate the target position and scale factor
    var targetWidth = window.innerWidth * 0.8;  // Fill 80% of the screen width
    var targetHeight = window.innerHeight * 0.8;  // Fill 80% of the screen height
    var scaleX = targetWidth / card.offsetWidth;
    var scaleY = targetHeight / card.offsetHeight;
    var targetLeft = (window.innerWidth - targetWidth) / 2 + window.scrollX;
    var targetTop = (window.innerHeight - targetHeight) / 2 + window.scrollY;

    // Apply the CSS properties
    card.style.position = 'fixed';
    card.style.top = `${targetTop}px`;
    card.style.left = `${targetLeft}px`;
    card.style.transform = `scale(${scaleX}, ${scaleY})`;
    card.style.zIndex = '10';

    document.querySelector('.overlay').classList.add('visible');
}

function collapseCard(card) {
    card.style.position = '';
    card.style.top = '';
    card.style.left = '';
    card.style.transform = '';
    card.style.zIndex = '';
}
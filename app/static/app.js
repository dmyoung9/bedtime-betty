function formatThemeButton(button, theme) {
    button.innerHTML = `${theme.emoji}<br>${theme.story_theme}`;
    button.style.backgroundColor = `${theme.color}`;
    button.style.color = `${theme.text_color}`;

    return button
}

function formatLessonButton(button, lesson) {
    button.textContent = `${lesson.story_lesson}`;

    return button
}

document.addEventListener('DOMContentLoaded', () => {
    const apiKey = localStorage.getItem('apiKey') || '';
    const wizard = new Wizard('wizardContainer', apiKey);

    // Add pages to the wizard with their respective source URLs
    wizard.addPage('ws://192.168.1.212:5000/api/stories/themes/stream', formatThemeButton);
    wizard.addPage('ws://192.168.1.212:5000/api/stories/lessons/stream ', formatLessonButton);


    // Load initial options for the first page
    wizard.start();

    // Add event listeners for Previous and Next buttons
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');

    prevButton.addEventListener('click', async() => {
        wizard.previousPage();
    });

    nextButton.addEventListener('click', async() => {
        wizard.nextPage();
    });
});
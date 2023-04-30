document.addEventListener('DOMContentLoaded', function () {
  const spinner = document.getElementById('spinner');
  const themesContainer = document.getElementById('themesContainer');
  const apiKey = localStorage.getItem('apiKey') || '';

  function showSpinner() {
    spinner.style.display = 'block';
  }

  function hideSpinner() {
    spinner.style.display = 'none';
  }

  function randomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  if (!apiKey) {
    alert('Please enter your API key on the settings page.');
    return;
  }

  function fetchThemes(apiKey) {
    showSpinner();

    fetch('http://192.168.1.212:5000/api/stories/themes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'OPENAI_API_KEY': apiKey
      },
      body: JSON.stringify({ num: 3 })
    })
      .then(response => response.json())
      .then(data => {
        themesContainer.innerHTML = ''; // Clear any existing buttons
        themesContainer.classList.add('d-flex', 'flex-column');
        data.forEach(theme => {
          const button = document.createElement('button');
          button.innerHTML = `${theme.emoji}<br>${theme.story_theme}`;
          button.style.backgroundColor = randomColor();
          button.style.border = 'none';
          button.classList.add('btn', 'btn-primary', 'mr-2', 'mb-2');
          themesContainer.appendChild(button);
        });
        hideSpinner();
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        hideSpinner();
      });
  }

  fetchThemes(apiKey);
});

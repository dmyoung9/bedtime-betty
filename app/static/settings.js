const settingsForm = document.getElementById('settingsForm');
const prefApiKeyInput = document.getElementById('prefApiKey');
const childAgeSlider = document.getElementById("childAge");

document.addEventListener('DOMContentLoaded', function () {
  // Load settings from localStorage
  const savedApiKey = localStorage.getItem('apiKey');
  const minAge = localStorage.getItem('minAge');
  const maxAge = localStorage.getItem('maxAge');

  if (savedApiKey) {
    prefApiKeyInput.value = savedApiKey;
  }

  // Initialize the noUiSlider with two handles
  noUiSlider.create(childAgeSlider, {
    start: [minAge || 2, maxAge || 7],
    connect: true,
    step: 1,
    range: {
      'min': 0,
      'max': 18
    }
  });

  // Update the age display when the slider values change
  childAgeSlider.noUiSlider.on('update', function (values, handle) {
    const minValue = Math.round(values[0]);
    const maxValue = Math.round(values[1]);
    document.getElementById("childAgeDisplay").textContent = `${minValue} - ${maxValue}`;
  });

  // Save settings to localStorage when the form is submitted
  settingsForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission

    localStorage.setItem('apiKey', prefApiKeyInput.value);
    localStorage.setItem('minAge', Math.round(childAgeSlider.noUiSlider.get(true)[0]));
    localStorage.setItem('maxAge', Math.round(childAgeSlider.noUiSlider.get(true)[1]));

    alert('settings saved successfully.');
  });
});
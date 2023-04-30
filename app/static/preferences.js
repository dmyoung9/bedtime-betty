document.addEventListener('DOMContentLoaded', function() {
    const preferencesForm = document.getElementById('preferencesForm');
    const prefApiKeyInput = document.getElementById('prefApiKey');
  
    // Load preferences from localStorage
    const savedApiKey = localStorage.getItem('apiKey');
    if (savedApiKey) {
      prefApiKeyInput.value = savedApiKey;
    }
  
    // Save preferences to localStorage when the form is submitted
    preferencesForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent form submission
  
      const apiKey = prefApiKeyInput.value;
      localStorage.setItem('apiKey', apiKey);
  
      alert('Preferences saved successfully.');
    });
  });
  
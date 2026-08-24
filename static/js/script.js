/**
 * script.js — Global script for AI Health Assistant
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Auto-calculate BMI in Profile Form on typing
  const heightInput = document.getElementById('heightInput');
  const weightInput = document.getElementById('weightInput');

  function autoCalculateBMI() {
    if (heightInput && weightInput) {
      const h = parseFloat(heightInput.value);
      const w = parseFloat(weightInput.value);
      if (h > 0 && w > 0) {
        const hm = h / 100.0;
        const bmi = (w / (hm * hm)).toFixed(1);
        console.log(`Calculated live BMI: ${bmi}`);
      }
    }
  }

  if (heightInput && weightInput) {
    heightInput.addEventListener('input', autoCalculateBMI);
    weightInput.addEventListener('input', autoCalculateBMI);
  }

  // 2. Auto-fade out flash messages after 6 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 6000);
  });
});

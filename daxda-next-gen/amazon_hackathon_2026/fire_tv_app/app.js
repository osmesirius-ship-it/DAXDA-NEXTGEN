/**
 * DAXDA Sentry — Fire TV App Logic
 * Designed for 10-foot TV viewing, D-Pad Remote Control, and Picture-in-Picture alerts.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Clock Updates
  const clockEl = document.getElementById('clock-display');
  function updateClock() {
    const now = new Date();
    clockEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  setInterval(updateClock, 1000);
  updateClock();

  // 2. D-Pad Remote Navigation System
  const focusables = Array.from(document.querySelectorAll('.focusable'));
  let currentFocusIndex = 0;

  function setFocus(index) {
    if (index >= 0 && index < focusables.length) {
      currentFocusIndex = index;
      focusables[currentFocusIndex].focus();
    }
  }

  // Initial focus on first element
  if (focusables.length > 0) {
    setFocus(0);
  }

  document.addEventListener('keydown', (e) => {
    const modal = document.getElementById('pip-modal');
    const isModalOpen = !modal.classList.contains('hidden');

    switch (e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        e.preventDefault();
        setFocus((currentFocusIndex + 1) % focusables.length);
        break;
      case 'ArrowUp':
      case 'ArrowLeft':
        e.preventDefault();
        setFocus((currentFocusIndex - 1 + focusables.length) % focusables.length);
        break;
      case 'Enter':
        // Trigger active focus click
        if (document.activeElement) {
          document.activeElement.click();
        }
        break;
      case 'Escape':
      case 'Back': // Fire TV Back Key
        if (isModalOpen) {
          dismissPip();
        }
        break;
    }
  });

  // 3. Picture-in-Picture Alert Demonstration
  const pipModal = document.getElementById('pip-modal');
  const btnDismiss = document.getElementById('pip-dismiss');
  const btnUnlock = document.getElementById('pip-unlock');
  const btnPlay = document.getElementById('btn-play');
  const btnCameras = document.getElementById('btn-cameras');
  const ringStatus = document.getElementById('ring-status-text');

  function showPipAlert(title, body) {
    document.getElementById('pip-title').textContent = title;
    document.getElementById('pip-body').textContent = body;
    pipModal.classList.remove('hidden');
    btnDismiss.focus();
  }

  function dismissPip() {
    pipModal.classList.add('hidden');
    setFocus(0);
  }

  btnDismiss.addEventListener('click', dismissPip);

  btnUnlock.addEventListener('click', () => {
    alert("DAXDA Governance Interceptor: Action 'UNLOCK_FRONT_DOOR' evaluated via AOG_1 Authority Gate: APPROVED with Cryptographic SHA-256 Receipt!");
    ringStatus.innerHTML = 'Door Lock: <strong style="color: #38bdf8;">UNLOCKED (GOVERNED)</strong> • 30s Auto-Relock Engaged';
    dismissPip();
  });

  btnPlay.addEventListener('click', () => {
    showPipAlert("MEDIA PLAYBACK GOVERNED", "Alexa+ adjusted volume to 25% because Bee Wearable detected an incoming phone call.");
  });

  btnCameras.addEventListener('click', () => {
    showPipAlert("RING MULTI-CAMERA VIEW", "Front Doorbell, Driveway Floodlight, and Backyard cameras synchronized in 4K quad-view.");
  });

  // Auto-demonstrate Ring doorbell ding after 4 seconds for video recording
  setTimeout(() => {
    showPipAlert(
      "RING PRO 2: VISITOR AT FRONT DOOR",
      "Courier detected with package. Alexa+ suggests: 'Ask Fire TV to unlock door or dismiss'."
    );
  }, 4000);
});

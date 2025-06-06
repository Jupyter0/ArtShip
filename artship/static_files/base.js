setTimeout(() => {
    const container = document.getElementById('messages');
    if (container) {
      container.style.transition = 'opacity 0.5s ease';
      container.style.opacity = '0';
      setTimeout(() => container.remove(), 500);
    }
}, 3000);
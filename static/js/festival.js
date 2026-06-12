// Скрипт для прокрутки мышкой (drag-to-scroll) на ПК версии
document.addEventListener("DOMContentLoaded", function() {
  const containers = document.querySelectorAll('.speakers-wrapper, .venues-wrapper');
  
  containers.forEach(container => {
    let isDown = false;
    let startX;
    let scrollLeft;
    
    container.addEventListener('mousedown', (e) => {
      isDown = true;
      container.classList.add('active-drag');
      startX = e.pageX - container.offsetLeft;
      scrollLeft = container.scrollLeft;
    });
    
    container.addEventListener('mouseleave', () => {
      isDown = false;
      container.classList.remove('active-drag');
    });
    
    // Слушаем отпускание кнопки мыши на уровне всего окна, чтобы избежать залипания
    window.addEventListener('mouseup', () => {
      if (isDown) {
        isDown = false;
        container.classList.remove('active-drag');
      }
    });
    
    container.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - container.offsetLeft;
      const walk = (x - startX) * 2; // скорость скролла
      container.scrollLeft = scrollLeft - walk;
    });

    // Отключаем дефолтное поведение перетаскивания (картинок, ссылок),
    // которое перехватывает фокус браузера и ломает событие mouseup
    container.addEventListener('dragstart', (e) => {
      e.preventDefault();
    });
  });
});

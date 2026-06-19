document.addEventListener('DOMContentLoaded', () => {
  const yearItems = document.querySelectorAll('.js-year-select');
  const knob = document.querySelector('.years-slider-knob');
  const timelineLine = document.querySelector('.years-timeline-line');
  const yearsNavList = document.querySelector('.years-nav-list');
  const navContainer = document.querySelector('.years-nav-container');
  
  if (!yearItems.length || !knob || !timelineLine) return;

  // Передвигает ползунок к элементу (теперь это полоска под годом)
  function moveKnobTo(element) {
    const rect = element.getBoundingClientRect();
    const parentRect = timelineLine.getBoundingClientRect();
    knob.style.left = `${element.offsetLeft}px`;
    knob.style.width = `${element.offsetWidth}px`;
  }

  // Центрирует активный год в контейнере
  function centerYear(element) {
    if (!navContainer) return;
    const containerWidth = navContainer.offsetWidth;
    const elementOffset = element.offsetLeft;
    const elementWidth = element.offsetWidth;
    
    navContainer.scrollTo({
      left: elementOffset - (containerWidth / 2) + (elementWidth / 2),
      behavior: 'smooth'
    });
  }

  // Находим активный элемент при загрузке страницы
  let activeItem = document.querySelector('.js-year-select.active') || yearItems[0];
  if (activeItem) {
    activeItem.classList.add('active');
    // Запуск позиционирования с небольшой задержкой, чтобы страница успела отрисоваться
    setTimeout(() => {
      moveKnobTo(activeItem);
      centerYear(activeItem);
    }, 300);
  }

  // Переключает описание проектов и слайдеры
  function switchYear(year) {
    // Переключаем проекты
    document.querySelectorAll('.js-project-detail').forEach(el => {
      if (el.getAttribute('data-year') === year) {
        el.style.display = 'block';
      } else {
        el.style.display = 'none';
      }
    });

    // Переключаем слайдеры (медиагалереи)
    document.querySelectorAll('.js-region-slider').forEach(el => {
      if (el.getAttribute('data-year') === year) {
        el.style.display = 'block';
      } else {
        el.style.display = 'none';
      }
    });

    // Переключаем баджи
    document.querySelectorAll('.js-region-badge').forEach(el => {
      if (el.getAttribute('data-year') === year) {
        el.style.display = 'inline-block';
      } else {
        el.style.display = 'none';
      }
    });
  }

  // Обработка событий для каждого года
  yearItems.forEach(item => {
    // Если год заблокирован (нет проекта), не вешаем обработчики
    if (item.classList.contains('disabled')) return;

    // При наведении курсора на год — ползунок бежит за ним (без переключения контента, чтобы не дергалось)
    item.addEventListener('mouseenter', () => {
      moveKnobTo(item);
    });

    // При клике фиксируем выбранный год как активный и переключаем контент
    item.addEventListener('click', () => {
      yearItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      activeItem = item;
      moveKnobTo(item);
      const year = item.getAttribute('data-year');
      switchYear(year);
    });
  });

  // Когда курсор покидает всю область выбора годов, ползунок возвращается к зафиксированному активному году
  if (yearsNavList) {
    yearsNavList.addEventListener('mouseleave', () => {
      if (activeItem) {
        moveKnobTo(activeItem);
      }
    });
  }

  // Пересчет позиции ползунка при изменении размеров экрана
  window.addEventListener('resize', () => {
    if (activeItem) {
      moveKnobTo(activeItem);
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const navList = document.querySelector('.navbar-nav');
  const underline = document.querySelector('.nav-underline-bar');
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

  if (!navList || !underline) return;

  // --- Shadow on Scroll effect ---
  const stickyMenu = document.querySelector('.nav-container-wrapper.sticky-top');
  const stickyHeaderRow = document.querySelector('.header-sticky-row');
  
  function handleScroll() {
    if (window.scrollY > 10) {
      if (stickyMenu) stickyMenu.classList.add('shadow-sm');
      if (stickyHeaderRow) stickyHeaderRow.classList.add('shadow-sm');
    } else {
      if (stickyMenu) stickyMenu.classList.remove('shadow-sm');
      if (stickyHeaderRow) stickyHeaderRow.classList.remove('shadow-sm');
    }
  }
  window.addEventListener('scroll', handleScroll);
  handleScroll(); // Initial check

  // --- Sliding Underline effect ---
  function alignUnderline(element) {
    if (!element) {
      underline.style.width = '0px';
      return;
    }
    
    const rect = element.getBoundingClientRect();
    const parentRect = navList.getBoundingClientRect();
    
    // We position the line exactly aligned to the text of the link
    underline.style.width = `${rect.width}px`;
    underline.style.left = `${rect.left - parentRect.left}px`;
  }

  // Check viewport size (only apply effect on large screens)
  function isDesktop() {
    return window.innerWidth >= 992;
  }

  // Hover event listeners
  navLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
      if (isDesktop()) {
        alignUnderline(link);
      }
    });
  });

  // Mouse leaves the navbar area - return to active link or disappear
  navList.addEventListener('mouseleave', () => {
    if (isDesktop()) {
      const activeLink = document.querySelector('.navbar-nav .nav-link.active');
      if (activeLink) {
        alignUnderline(activeLink);
      } else {
        underline.style.width = '0px';
      }
    }
  });

  // Recalculate on window resize
  window.addEventListener('resize', () => {
    if (isDesktop()) {
      const activeLink = document.querySelector('.navbar-nav .nav-link.active');
      if (activeLink) {
        alignUnderline(activeLink);
      } else {
        underline.style.width = '0px';
      }
    } else {
      underline.style.width = '0px';
    }
  });

  // Setup active status based on URL pathname (helpful for dynamic routing)
  const currentPath = window.location.pathname;
  let hasActive = false;
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '#' && currentPath.startsWith(href)) {
      link.classList.add('active');
      hasActive = true;
    }
  });

  // Initial alignment on page load
  setTimeout(() => {
    if (isDesktop()) {
      const activeLink = document.querySelector('.navbar-nav .nav-link.active');
      if (activeLink) {
        alignUnderline(activeLink);
      }
    }
  }, 200); // Small timeout to allow styles/fonts to load and calculate correctly

  // --- Interactive Map Logic ---
  const mapElement = document.querySelector('.js-history-competition-map');
  const mapTooltip = document.querySelector('.js-history-competition-label-region-hover');

  const regionNames = {
    'PETERSBURG': 'Санкт-Петербург',
    'ARHANGELSKAYA_OBLAST': 'Архангельская область',
    'BELGOROD': 'Белгородская область',
    'VORONEZH': 'Воронежская область',
    'ULYANOVSK': 'Ульяновская область',
    'NOVOSIBIRSKAYA_OBLAST': 'Новосибирская область',
    'IRKUTSK': 'Иркутская область',
    'TATARSTAN': 'Республика Татарстан',
    'YAKUTIYA': 'Республика Саха (Якутия)',
    'RESPUBLIKA_BASHKORTOSTAN': 'Республика Башкортостан',
    'KURSKAYA_OBLAST': 'Курская область'
  };

  if (mapElement && mapTooltip) {
    const regions = mapElement.querySelectorAll('.js-history-competition-region');
    const container = mapElement.closest('.map-container-wrapper') || mapElement.closest('.map-card-wrapper') || mapElement.closest('.position-relative') || mapElement.closest('.col-lg-6');
    const winnerCard = document.querySelector('.js-winner-card');

    // Убеждаемся, что контейнер имеет относительное позиционирование для тултипа
    if (container) {
      container.style.position = 'relative';
    }

    regions.forEach(region => {
      region.addEventListener('mouseenter', () => {
        const regionId = region.getAttribute('id');
        mapTooltip.textContent = regionNames[regionId] || regionId;
        mapTooltip.style.display = 'block';
      });

      region.addEventListener('mousemove', (e) => {
        if (!container) return;
        const containerRect = container.getBoundingClientRect();
        
        // Позиционируем тултип относительно контейнера с учетом прокрутки
        // x: +15px вправо от курсора
        // y: -45px вверх от курсора (чтобы он был НАД курсором и не вызывал скролл)
        const x = e.clientX - containerRect.left + container.scrollLeft + 20;
        const y = e.clientY - containerRect.top + container.scrollTop - 20;
        
        mapTooltip.style.left = `${x}px`;
        mapTooltip.style.top = `${y}px`;
      });

      region.addEventListener('mouseleave', () => {
        mapTooltip.style.display = 'none';
      });

      // Обработка выбора региона при клике
      region.addEventListener('click', () => {
        const regionId = region.getAttribute('id');
        const regionDataEl = document.querySelector(`.js-map-region-item[data-svg-id="${regionId}"]`);

        if (regionDataEl && winnerCard) {
          const title = regionDataEl.getAttribute('data-title');
          const text = regionDataEl.getAttribute('data-text');
          const coat = regionDataEl.getAttribute('data-coat');
          const years = regionDataEl.getAttribute('data-years');
          const url = regionDataEl.getAttribute('data-url');

          const cardTitle = winnerCard.querySelector('.js-winner-title');
          const cardYear = winnerCard.querySelector('.js-winner-year');
          const cardText = winnerCard.querySelector('.js-winner-text');
          const cardCoat = winnerCard.querySelector('.js-winner-coat');
          const cardCoatContainer = winnerCard.querySelector('.js-winner-coat-container');
          const cardContentContainer = winnerCard.querySelector('.js-winner-content-container');
          const cardLink = winnerCard.querySelector('.js-winner-link');

          // Заполняем данные карточки
          if (cardTitle) cardTitle.textContent = title;
          
          if (cardYear) {
            if (years) {
              cardYear.textContent = years;
              cardYear.style.display = '';
            } else {
              cardYear.style.display = 'none';
            }
          }

          if (cardText) {
            // Если текст пустой, выводим стандартную заглушку или очищаем
            cardText.innerHTML = text ? text.replace(/\n/g, '<br>') : 'Информация о проектах региона в рамках конкурса.';
          }

          if (cardCoat && cardCoatContainer && cardContentContainer) {
            if (coat) {
              cardCoat.setAttribute('src', coat);
              cardCoatContainer.style.display = '';
              cardContentContainer.className = 'col js-winner-content-container';
            } else {
              cardCoatContainer.style.display = 'none';
              cardContentContainer.className = 'col-12 js-winner-content-container';
            }
          }

          if (cardLink) {
            let finalUrl = url;
            if (years) {
              const yearList = years.split(',').map(y => y.trim()).filter(Boolean);
              if (yearList.length > 0) {
                const lastYear = yearList[yearList.length - 1];
                finalUrl = `/${lastYear}-contest/`;
              }
            }
            if (finalUrl) {
              cardLink.setAttribute('href', finalUrl);
              cardLink.style.display = '';
            } else {
              cardLink.style.display = 'none';
            }
          }

          // Убираем подсветку со всех регионов и подсвечиваем кликнутый
          regions.forEach(r => r.classList.remove('is-selected'));
          region.classList.add('is-selected');

          // Плавно показываем карточку с анимацией
          winnerCard.classList.remove('d-none');
          winnerCard.style.opacity = '0';
          winnerCard.style.transform = 'translateY(10px)';
          winnerCard.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
          
          // Триггер перерисовки для запуска анимации
          winnerCard.offsetHeight;
          
          winnerCard.style.opacity = '1';
          winnerCard.style.transform = 'translateY(0)';
        } else {
          // Если регион не заведен в базу, скрываем карточку и снимаем выделение
          if (winnerCard) {
            regions.forEach(r => r.classList.remove('is-selected'));
            winnerCard.style.opacity = '0';
            winnerCard.style.transform = 'translateY(10px)';
            winnerCard.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            setTimeout(() => {
              winnerCard.classList.add('d-none');
            }, 400);
          }
        }
      });
    });

    // --- Автоматически выбираем регион текущего года по умолчанию ---
    const currentYear = new Date().getFullYear(); // 2026
    let defaultRegionData = Array.from(document.querySelectorAll('.js-map-region-item')).find(el => {
      const years = el.getAttribute('data-years') || '';
      return years.split(', ').map(y => y.trim()).includes(String(currentYear));
    });

    // Если победителя за текущий год в базе нет, берем регион с самым последним годом победы
    if (!defaultRegionData) {
      defaultRegionData = Array.from(document.querySelectorAll('.js-map-region-item')).sort((a, b) => {
        const yearsA = (a.getAttribute('data-years') || '').split(', ').map(Number);
        const yearsB = (b.getAttribute('data-years') || '').split(', ').map(Number);
        const maxA = yearsA.length ? Math.max(...yearsA) : 0;
        const maxB = yearsB.length ? Math.max(...yearsB) : 0;
        return maxB - maxA;
      })[0];
    }

    if (defaultRegionData) {
      const svgId = defaultRegionData.getAttribute('data-svg-id');
      const regionEl = mapElement.querySelector(`#${svgId}`);
      if (regionEl) {
        // Триггерим клик, чтобы карточка отобразилась по умолчанию
        regionEl.dispatchEvent(new Event('click'));
      }
    }
  }

  // --- Read More Toggle ---
  const readMoreBtn = document.querySelector('.js-read-more');
  const readMoreWrapper = document.querySelector('.read-more-wrapper');
  const readMoreContainer = document.querySelector('.read-more-container');

  if (readMoreBtn && readMoreWrapper && readMoreContainer) {
    readMoreBtn.addEventListener('click', function(e) {
      e.preventDefault();
      readMoreContainer.classList.add('expanded');
      readMoreWrapper.classList.remove('collapsed');
      
      // Плавно увеличиваем высоту до реального размера контента
      const fullHeight = readMoreWrapper.scrollHeight;
      readMoreWrapper.style.maxHeight = fullHeight + 'px';
      
      // После завершения анимации убираем лимит высоты совсем
      setTimeout(() => {
        readMoreWrapper.style.maxHeight = 'none';
      }, 800);
    });
  }

  // --- Mobile Menu: Lock Scroll ---
  const mainNavbar = document.getElementById('mainNavbar');
  if (mainNavbar) {
    mainNavbar.addEventListener('show.bs.collapse', function () {
      document.body.classList.add('menu-open');
    });
    mainNavbar.addEventListener('hidden.bs.collapse', function () {
      document.body.classList.remove('menu-open');
    });
  }

  // --- Regions List: Search and Collapse ---
  const regionSearchInput = document.querySelector('.js-region-search');
  const regionsContainer = document.querySelector('.js-regions-container');
  const regionItems = document.querySelectorAll('.js-region-item');
  const regionColumns = document.querySelectorAll('.js-region-column');

  // Инициализация: сворачиваем список на мобильных (стили в CSS через медиа-запрос)
  if (regionsContainer) {
    regionsContainer.classList.add('collapsed');
  }

  // Поиск и фильтрация
  if (regionSearchInput) {
    regionSearchInput.addEventListener('input', function() {
      const query = this.value.toLowerCase().trim();
      
      // Добавляем класс, если поиск активен, чтобы убрать градиент и ограничение высоты
      if (query.length > 0) {
        regionsContainer.classList.add('is-searching');
      } else {
        regionsContainer.classList.remove('is-searching');
      }
      
      regionItems.forEach(item => {
        const name = item.getAttribute('data-name');
        if (name.includes(query)) {
          item.classList.remove('d-none-search');
        } else {
          item.classList.add('d-none-search');
        }
      });

      // Скрываем пустые группы букв
      const letterGroups = document.querySelectorAll('.js-letter-group');
      letterGroups.forEach(group => {
        const visibleInGroup = group.querySelectorAll('.js-region-item:not(.d-none-search)');
        if (visibleInGroup.length === 0) {
          group.style.display = 'none';
        } else {
          group.style.display = 'block';
        }
      });

      // Скрываем пустые колонки
      regionColumns.forEach(col => {
        const visibleItems = col.querySelectorAll('.js-region-item:not(.d-none-search)');
        if (visibleItems.length === 0) {
          col.style.display = 'none';
        } else {
          col.style.display = 'block';
        }
      });
    });
  }

  // --- Custom Cursor Follower ---
  const follower = document.querySelector('.cursor-follower');
  if (follower) {
    let mouseX = 0;
    let mouseY = 0;
    let followerX = 0;
    let followerY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (follower.style.opacity === '0' || follower.style.opacity === '') {
        follower.style.opacity = '1';
        followerX = mouseX;
        followerY = mouseY;
      }
    });

    document.addEventListener('mouseleave', () => {
      follower.style.opacity = '0';
    });

    function animateFollower() {
      // Плавное следование за мышью
      let dx = mouseX - followerX;
      let dy = mouseY - followerY;
      
      followerX += dx * 0.1;
      followerY += dy * 0.1;
      
      follower.style.left = followerX + 'px';
      follower.style.top = followerY + 'px';
      
      requestAnimationFrame(animateFollower);
    }
    animateFollower();
  }
});

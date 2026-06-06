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
    const container = mapElement.closest('.map-card-wrapper') || mapElement.closest('.position-relative') || mapElement.closest('.col-lg-6');

    regions.forEach(region => {
      region.addEventListener('mouseenter', () => {
        const regionId = region.getAttribute('id');
        mapTooltip.textContent = regionNames[regionId] || regionId;
        mapTooltip.style.display = 'block';
      });

      region.addEventListener('mousemove', (e) => {
        if (!container) return;
        const containerRect = container.getBoundingClientRect();
        
        // Position tooltip relative to map card container
        const x = e.clientX - containerRect.left + 15;
        const y = e.clientY - containerRect.top + 15;
        
        mapTooltip.style.left = `${x}px`;
        mapTooltip.style.top = `${y}px`;
      });

      region.addEventListener('mouseleave', () => {
        mapTooltip.style.display = 'none';
      });
    });
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
  const regionsExpandBtn = document.querySelector('.js-regions-expand');
  const regionItems = document.querySelectorAll('.js-region-item');
  const regionColumns = document.querySelectorAll('.js-region-column');

  // Инициализация: сворачиваем список на мобильных
  if (regionsContainer) {
    regionsContainer.classList.add('collapsed');
  }

  // Поиск и фильтрация
  if (regionSearchInput) {
    regionSearchInput.addEventListener('input', function() {
      const query = this.value.toLowerCase().trim();
      
      // Если есть поиск - автоматически разворачиваем список
      if (query.length > 0 && regionsContainer.classList.contains('collapsed')) {
        toggleRegions();
      }

      regionItems.forEach(item => {
        const name = item.getAttribute('data-name');
        if (name.includes(query)) {
          item.classList.remove('d-none-search');
        } else {
          item.classList.add('d-none-search');
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

  // Логика разворачивания/сворачивания
  function toggleRegions() {
    if (!regionsContainer) return;
    
    const isCollapsed = regionsContainer.classList.contains('collapsed');
    const list = regionsContainer.querySelector('.js-regions-list');
    const btnText = regionsExpandBtn.querySelector('span');
    const btnIcon = regionsExpandBtn.querySelector('i');

    if (isCollapsed) {
      // РАЗВОРАЧИВАЕМ
      regionsContainer.classList.remove('collapsed');
      regionsContainer.classList.add('expanded');
      
      const fullHeight = list.scrollHeight;
      list.style.maxHeight = fullHeight + 'px';
      
      if (btnText) btnText.textContent = 'Свернуть список';
      if (btnIcon) {
        btnIcon.classList.remove('bi-chevron-down');
        btnIcon.classList.add('bi-chevron-up');
      }

      // После завершения анимации разрешаем контенту расти свободно
      setTimeout(() => {
        if (regionsContainer.classList.contains('expanded')) {
          list.style.maxHeight = 'none';
        }
      }, 600);
    } else {
      // СВОРАЧИВАЕМ
      // Сначала устанавливаем текущую высоту в px вместо 'none', чтобы анимация сработала
      list.style.maxHeight = list.scrollHeight + 'px';
      
      // Небольшая задержка, чтобы браузер успел применить maxHeight в px
      requestAnimationFrame(() => {
        regionsContainer.classList.remove('expanded');
        regionsContainer.classList.add('collapsed');
        list.style.maxHeight = '320px'; // Возвращаем к высоте из CSS
        
        if (btnText) btnText.textContent = 'Показать все регионы';
        if (btnIcon) {
          btnIcon.classList.remove('bi-chevron-up');
          btnIcon.classList.add('bi-chevron-down');
        }
      });

      // Скроллим к началу списка, если пользователь свернул его, будучи внизу
      regionsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  if (regionsExpandBtn) {
    regionsExpandBtn.addEventListener('click', toggleRegions);
  }
});

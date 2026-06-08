document.addEventListener("DOMContentLoaded", function() {
    // 1 строка: Центрирование активного года на мобилках
    const activeYear = document.querySelector(".year-list .btn-year.active");
    if (activeYear && window.innerWidth < 992) {
      activeYear.scrollIntoView({ behavior: "auto", inline: "center", block: "nearest" });
    }

    // 8 строка: Синхронизация селекта и табов в Коротком Списке
    const select = document.querySelector(".js-shortlist-select");
    const tabButtons = document.querySelectorAll('.short-list-item[data-bs-toggle="pill"]');
    
    if (select) {
      // Из селекта в табы
      select.addEventListener("change", function() {
        const regionId = this.value;
        const tabButton = document.getElementById(`tab-${regionId}`);
        if (tabButton) {
          const tab = new bootstrap.Tab(tabButton);
          tab.show();
        }
      });

      // Из табов в селект (при клике на десктопе)
      tabButtons.forEach(btn => {
        btn.addEventListener('shown.bs.tab', function (event) {
          const regionId = event.target.id.replace('tab-', '');
          select.value = regionId;
        });
      });
    }

    // 8 строка: Интерактив градиентной подложки в Коротком Списке (только для десктопа)
    const container = document.querySelector(".short-list-container");
    const hoverBg = document.querySelector(".shortlist-hover-bg");
    const items = document.querySelectorAll(".short-list-item");

    if (container && hoverBg && window.innerWidth >= 992) {
      items.forEach(item => {
        item.addEventListener("mouseenter", function() {
          const rect = item.getBoundingClientRect();
          const containerRect = container.getBoundingClientRect();
          
          // Вычисляем относительную позицию элемента внутри контейнера
          const relativeTop = rect.top - containerRect.top;
          const relativeLeft = rect.left - containerRect.left;
          
          // Задаем геометрию подложке
          hoverBg.style.top = relativeTop + "px";
          hoverBg.style.left = relativeLeft + "px";
          hoverBg.style.width = rect.width + "px";
          hoverBg.style.height = rect.height + "px";
          hoverBg.style.opacity = "1";
        });
      });

      // При выходе мыши из контейнера списка - скрываем подложку
      container.addEventListener("mouseleave", function() {
        hoverBg.style.opacity = "0";
      });
    }

    // 6 строка: Логика "Читать дальше" для описания победителя
    const descContent = document.querySelector(".winner-project-description-content");
    const descBtn = document.querySelector(".js-winner-read-more-btn");
    const descFade = document.querySelector(".winner-description-fade");

    if (descContent && descBtn && descFade) {
      const collHeight = 250;
      if (descContent.scrollHeight <= collHeight) {
        descBtn.parentElement.style.display = "none";
        descFade.style.display = "none";
        descContent.classList.remove("winner-description-collapsed");
        descContent.style.maxHeight = "none";
      } else {
        descContent.style.maxHeight = collHeight + "px";
        
        descBtn.addEventListener("click", function() {
          if (descContent.classList.contains("winner-description-collapsed")) {
            descContent.classList.remove("winner-description-collapsed");
            descContent.classList.add("winner-description-expanded");
            descContent.style.maxHeight = descContent.scrollHeight + "px";
            descFade.style.opacity = "0";
            descBtn.innerHTML = 'Свернуть &uarr;';
          } else {
            descContent.classList.remove("winner-description-expanded");
            descContent.classList.add("winner-description-collapsed");
            descContent.style.maxHeight = collHeight + "px";
            descFade.style.opacity = "1";
            descBtn.innerHTML = 'Читать дальше &darr;';
            
            descContent.scrollIntoView({ behavior: "smooth", block: "nearest" });
          }
        });
      }
    }
  });

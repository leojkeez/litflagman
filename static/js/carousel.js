document.addEventListener("DOMContentLoaded", function() {
    const carousels = document.querySelectorAll(".carousel-custom");
    
    carousels.forEach(carouselEl => {
        let startX = 0;
        let endX = 0;
        let isDragging = false;

        carouselEl.addEventListener('mousedown', (e) => {
            startX = e.pageX;
            isDragging = true;
            carouselEl.style.cursor = 'grabbing';
        });

        carouselEl.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            endX = e.pageX;
        });

        const handleDragEnd = () => {
            if (!isDragging) return;
            isDragging = false;
            carouselEl.style.cursor = 'grab';

            const diffX = endX - startX;
            const threshold = 60; // Порог сдвига мыши в пикселях для переключения

            if (Math.abs(diffX) > threshold) {
                // Подключаемся к Bootstrap Carousel API
                const carousel = bootstrap.Carousel.getOrCreateInstance(carouselEl);
                if (diffX > 0) {
                    carousel.prev();
                } else {
                    carousel.next();
                }
            }
            startX = 0;
            endX = 0;
        };

        window.addEventListener('mouseup', handleDragEnd);
        carouselEl.addEventListener('mouseleave', handleDragEnd);

        carouselEl.querySelectorAll('img').forEach(img => {
            img.addEventListener('dragstart', (e) => e.preventDefault());
        });

        // Синхронизация активной превьюшки при смене слайда
        carouselEl.addEventListener('slide.bs.carousel', (e) => {
            const index = e.to;
            const parentEl = carouselEl.parentElement;
            if (parentEl) {
                const thumbnailsContainer = parentEl.querySelector('.carousel-thumbnails');
                const thumbnails = parentEl.querySelectorAll('.thumbnail-item');
                
                thumbnails.forEach((thumb, i) => {
                    if (i === index) {
                        thumb.classList.add('active');
                        
                        // Скроллим только контейнер превью, не затрагивая страницу
                        if (thumbnailsContainer) {
                            const containerWidth = thumbnailsContainer.offsetWidth;
                            const thumbOffset = thumb.offsetLeft;
                            const thumbWidth = thumb.offsetWidth;
                            
                            thumbnailsContainer.scrollTo({
                                left: thumbOffset - (containerWidth / 2) + (thumbWidth / 2),
                                behavior: 'smooth'
                            });
                        }
                    } else {
                        thumb.classList.remove('active');
                    }
                });
            }
        });
    });
});

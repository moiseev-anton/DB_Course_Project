document.getElementById('filter-form').addEventListener('submit', function(event) {
        // Отключаем стандартное поведение формы
        event.preventDefault();

        // Создаем новый URL
        const formData = new FormData(this);
        const params = new URLSearchParams();

        // Добавляем только непустые поля
        for (const [key, value] of formData.entries()) {
            if (value !== "") {
                params.append(key, value);
            }
        }

        // Перенаправляем на новый URL
        const newUrl = new URL(window.location.href);
        newUrl.search = params.toString();
        window.location.replace(newUrl.toString());
    });
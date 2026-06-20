// Утилита для чтения CSRF-токена из cookie (рекомендованный Django способ)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Обновляет счётчик товаров в навбаре
function updateCartCounter(totalQuantity) {
    const counter = document.getElementById('cart-counter');
    if (counter) {
        counter.textContent = totalQuantity;
    }
}

// Добавление товара в корзину (кнопка "В корзину" на странице товара)
document.querySelectorAll('.add-to-cart-btn').forEach(function (button) {
    button.addEventListener('click', function () {
        const variantId = button.dataset.variantId;

        fetch(`/cart/add/${variantId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    updateCartCounter(data.total_quantity);
                }
            });
    });
});

// Изменение количества товара в корзине (на странице корзины)
document.querySelectorAll('.cart-qty-input').forEach(function (input) {
    input.addEventListener('change', function () {
        const itemId = input.dataset.itemId;
        const quantity = input.value;

        fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `quantity=${quantity}`,
        })
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    return;
                }

                updateCartCounter(data.total_quantity);

                const row = document.querySelector(`tr[data-item-id="${itemId}"]`);

                if (quantity <= 0) {
                    if (row) {
                        row.remove();
                    }
                    checkIfCartEmpty();
                    return;
                }

                const itemTotalCell = document.querySelector(`.cart-item-total[data-item-id="${itemId}"]`);
                if (itemTotalCell) {
                    itemTotalCell.textContent = `${data.item_total} ₽`;
                }

                const totalPriceEl = document.getElementById('cart-total-price');
                if (totalPriceEl) {
                    totalPriceEl.textContent = data.cart_total;
                }
            });
    });
});

// Удаление товара из корзины
document.querySelectorAll('.cart-remove-btn').forEach(function (button) {
    button.addEventListener('click', function () {
        const itemId = button.dataset.itemId;

        fetch(`/cart/delete/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    return;
                }

                updateCartCounter(data.total_quantity);

                const row = document.querySelector(`tr[data-item-id="${itemId}"]`);
                if (row) {
                    row.remove();
                }
                checkIfCartEmpty();
            });
    });
});

// Проверяет, не опустела ли корзина, и показывает сообщение, если да
function checkIfCartEmpty() {
    const tbody = document.getElementById('cart-items-body');
    if (tbody && tbody.children.length === 0) {
        const table = tbody.closest('table');
        if (table) {
            table.parentElement.remove();
        }
        const container = document.querySelector('.container.py-5');
        if (container && !document.getElementById('cart-empty-message')) {
            const p = document.createElement('p');
            p.className = 'text-muted';
            p.id = 'cart-empty-message';
            p.textContent = 'Ваша корзина пуста.';
            container.appendChild(p);
        }
    }
}
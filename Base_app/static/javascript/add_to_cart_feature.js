document.addEventListener("DOMContentLoaded", function () {
    // Initialize cart count
    updateCartCount();

    // Add event listeners for add-to-cart buttons
    document.querySelectorAll(".add-btn").forEach(button => {
        button.addEventListener("click", addToCart);
    });

    // Event delegation for cart actions
    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("delete-btn")) {
            deleteCartItem(event);
        }
    });
});

function addToCart() {
    const productId = this.getAttribute("data-id").trim();
    const productType = this.getAttribute("data-type").trim();

    fetch("/add-to-cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ 
            product_id: productId, 
            product_type: productType 
        })
    })
    .then(response => {
        // First check if response is JSON
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new TypeError("Server didn't return JSON");
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("Added to cart!");
            // Always use the server's cart count instead of incrementing locally
            updateCartCount();
        } else {
            throw new Error(data.message || "Failed to add to cart");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        if (error.message.includes("login")) {
            window.location.href = "/login/";
        } else {
            alert("Error: " + error.message);
        }
    });
}

function deleteCartItem(event) {
    const itemId = event.target.getAttribute("data-item-id");

    fetch("/cart/remove/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ item_id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove item row
            event.target.closest("tr")?.remove();
            
            // Update UI
            updateOrderSummary(data.subtotal, data.tax, data.total);
            updateCartCount();
            
            // Handle empty cart
            if (data.cart_count === 0) {
                showEmptyCartMessage();
            }
        } else {
            throw new Error(data.message || "Failed to remove item");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error: " + error.message);
    });
}

function updateCartCount() {
    fetch("/cart/count/")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const cartBadge = document.getElementById("cart-count");
                if (cartBadge) {
                    cartBadge.textContent = data.count;
                }
            }
        })
        .catch(error => console.error("Error updating cart count:", error));
}

function showEmptyCartMessage() {
    document.querySelector(".cart-table").style.display = "none";
    document.querySelector(".cart-summary").style.display = "none";
    document.querySelector(".cart-actions").style.display = "none";

    const cartContainer = document.querySelector(".cart-container");
    cartContainer.innerHTML = `
        <p class="empty-cart-message">Your cart is empty.</p>
        <a href="/" class="continue-shopping">Continue Shopping</a>
    `;
}

function updateOrderSummary(subtotal, tax, total) {
    document.getElementById("subtotal").textContent = `$${subtotal}`;
    document.getElementById("tax").textContent = `$${tax}`;
    document.getElementById("total").textContent = `$${total}`;
}

function getCSRFToken() {
    const cookie = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='));
    if (!cookie) {
        console.error("CSRF token not found!");
        return null;
    }
    return cookie.split('=')[1];
}
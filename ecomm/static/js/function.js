document.getElementById("reviewForm").addEventListener("submit", function(event) {
    event.preventDefault();
    console.log("Form submission triggered");

    let formData = new FormData(this);
    let url = this.action;
    console.log("Submitting to URL:", url);

    fetch(url, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
        body: formData,
    })
    .then(response => {
        console.log("Response received", response);
        return response.json();
    })
    .then(data => {
        console.log("Data received", data);
        if (data.bool) {
            // Update the review count
            let reviewCount = document.getElementById("review-count");
            reviewCount.innerText = parseInt(reviewCount.innerText) + 1;

            // Create a new review element
            let newReview = document.createElement("div");
            newReview.classList.add("review-box");
            newReview.style.marginTop = "20px";
            newReview.style.padding = "15px";
            newReview.style.backgroundColor = "#f9f9f9";
            newReview.style.borderRadius = "5px";
            
            newReview.innerHTML = `
                <p style="font-size: 14px; font-weight: bold; color: #ea1d6f;">${data.context.user}</p>
                <p style="font-size: 12px; color: #555555; line-height: 1.6;">
                    ${"★".repeat(data.context.rating)}${"☆".repeat(5 - data.context.rating)} (Rating: ${data.context.rating} / 5)
                </p>
                <p style="font-size: 12px; color: #555555; line-height: 1.6;">${data.context.review}</p>
                <p style="font-size: 12px; color: #999;">Reviewed on: ${new Date().toLocaleDateString()}</p>
            `;

            // Append the new review to the review list
            document.getElementById("review-list").prepend(newReview); // Add the new review at the top
            document.getElementById("reviewForm").reset(); // Reset the form

            // Hide the "Leave a Review" button
            let leaveReviewButton = document.getElementById("leaveReviewButton");
            if (leaveReviewButton) {
                leaveReviewButton.style.display = "none";
            }

            // Display success message
            let successMessage = document.getElementById("successMessage");
            successMessage.innerText = "Review submitted successfully!";
            successMessage.style.display = "block";
        }
    })
    .catch(error => console.error("Error:", error));
});

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("viewAllReviews").onclick = function() {
        document.getElementById("more-reviews").style.display = "block";
        this.style.display = "none"; // Hide the "View All" button after clicking
    };
});


document.addEventListener("DOMContentLoaded", function () {
    const addToCartButton = document.querySelector(".cart-button");
    const cartCountElement = document.getElementById("cart-count");

    if (addToCartButton) {
        addToCartButton.addEventListener("click", function (event) {
            event.preventDefault();

            // Check if user is not logged in
            if (addToCartButton.classList.contains("login-required")) {
                alert("You need to log in to add items to the cart.");
                return;
            }
            
            // Check if product is out of stock
            if (addToCartButton.classList.contains("disabled")) {
                alert("Sorry, this product is out of stock.");
                return;
            }

            // Retrieve product details
            const quantity = document.getElementById("quantity").value;
            const productId = document.getElementById("product_id").value;
            const productTitle = document.getElementById("product_title").value;

            // Send AJAX request to add the item to the cart
            fetch("/cart/add/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `product_id=${productId}&quantity=${quantity}&product_title=${productTitle}`
            })
            .then(response => {
                if (response.status === 401) {
                    alert("You need to log in to add items to the cart.");
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data && data.success) {
                    cartCountElement.textContent = data.cart_count;
                    alert(`${productTitle} has been added to your cart!`);
                } else if (data) {
                    alert(data.message || "An error occurred.");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }

    function getCSRFToken() {
        return document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1] || "";
    }


    $.ajax({
        url: '/add-to-cart',
        type: 'GET',
        data: {
            "pid": product_id,          // Replace with actual product ID variable
            "qty": quantity,           // Replace with actual quantity variable
            "title": product_title,    // Replace with actual title variable
            "price": product_price     // Replace with actual price variable
        },
        dataType: 'json',
        beforeSend: function() {
            console.log("Adding Product to Cart...");
        },
        success: function(response) {
            this_val.html("Item added to cart"); // Replace `this_val` with the actual element selector
            console.log("Added Product to Cart!");
    
            // Update the cart items count in the HTML
            $('.cart-items-count').text(response.totalcartitems);
        },
        error: function(xhr, status, error) {
            console.log("Error adding product to cart:", error);
        }
    });
    
});

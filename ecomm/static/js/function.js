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

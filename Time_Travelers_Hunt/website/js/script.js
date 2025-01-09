// Function to handle fade-in on scroll
document.addEventListener('DOMContentLoaded', function () {
    // Select all sections you want to fade in
    const fadeElements = document.querySelectorAll('.fade-in');

    // Set up an intersection observer
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            // If the element is in the viewport, add the 'visible' class
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Stop observing after it's visible
            }
        });
    }, {
        threshold: 0.3 // Trigger when 30% of the element is in the viewport
    });

    // Observe each element that needs fade-in
    fadeElements.forEach(element => {
        observer.observe(element);
    });
});

// Select all "Read More" buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.read-more-btn'); // Select all Read More buttons

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const extraContent = this.previousElementSibling; // Get the .extra-content div before the button
            
            if (extraContent.style.display === "none" || extraContent.style.display === "") {
                extraContent.style.display = "block"; // Show the extra content
                this.textContent = "Read Less"; // Change button text
            } else {
                extraContent.style.display = "none"; // Hide the extra content
                this.textContent = "Read More"; // Change button text back
            }
        });
    });
});
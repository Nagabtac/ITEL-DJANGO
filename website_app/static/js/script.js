const button = document.getElementById("btn");
const image = document.getElementById("mainImage");

let currentImage = 1;
const totalImages = 6;


// button.addEventListener("mouseenter", function() {
//     button.style.backgroundColor = "#6b4c7a";  // darker purple
// });

// button.addEventListener("mouseleave", function() {
//     button.style.backgroundColor = "#a45fa6";  // original purple
// });

/* 🔹 CLICK = CHANGE IMAGE */
button.addEventListener("click", function() {
    currentImage++;

    if (currentImage > totalImages) {
        currentImage = 1;
    }

    image.src = `/static/images/image${currentImage}.jpg`;
});
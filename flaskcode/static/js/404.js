document.addEventListener("DOMContentLoaded", function() {
    const elements = document.querySelectorAll('.animated');
    elements.forEach(element => {
        element.addEventListener('mouseover', function() {
            element.classList.add('highlight');
        });
        element.addEventListener('mouseout', function() {
            element.classList.remove('highlight');
        });
    });
});

// // Additional CSS for the highlight effect
// document.head.insertAdjacentHTML("beforeend", `<style>
// .highlight {
//     animation: none;
//     color: #ff5722 !important;
// }
// </style>`);

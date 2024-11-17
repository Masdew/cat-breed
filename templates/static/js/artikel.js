 // Adjust padding based on the page URL
 document.addEventListener("DOMContentLoaded", function() {
    const path = window.location.pathname;

    if (path.includes("artikel1")) {
        document.querySelector(".article-content").style.paddingTop = "100px";
    } else if (path.includes("artikel2")) {
        document.querySelector(".article-content").style.paddingTop = "100px";
    } else if (path.includes("artikel3")) {
        document.querySelector(".article-content").style.paddingTop = "100px";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".menu-toggle");
    const navigation = document.querySelector("#nav");

    if (!menuButton || !navigation) {
        return;
    }

    menuButton.addEventListener("click", function () {
        const isExpanded =
            menuButton.getAttribute("aria-expanded") === "true";

        menuButton.setAttribute("aria-expanded", String(!isExpanded));
        navigation.classList.toggle("nav-open", !isExpanded);
    });

    navigation.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            menuButton.setAttribute("aria-expanded", "false");
            navigation.classList.remove("nav-open");
        });
    });
});


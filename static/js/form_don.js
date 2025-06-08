document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formulaire_don");

    form.addEventListener("submit", (e) => {
        // Add info fields
        const partie1 = JSON.parse(sessionStorage.getItem("formulaire_partie1")) || {};
        Object.entries(partie1).forEach(([key, value]) => {
            const hidden = document.createElement("input");
            hidden.type = "hidden";
            hidden.name = key;
            hidden.value = String(value);
            form.appendChild(hidden);
        });

        // Add test fields
        const partie2 = JSON.parse(sessionStorage.getItem("formulaire_partie2")) || {};
        Object.entries(partie2).forEach(([key, value]) => {
            const hidden = document.createElement("input");
            hidden.type = "hidden";
            hidden.name = key;
            hidden.value = String(value);
            form.appendChild(hidden);
        });

        // Clear sessionStorage after final submit
        sessionStorage.removeItem("formulaire_partie1");
        sessionStorage.removeItem("formulaire_partie2");
    });
});
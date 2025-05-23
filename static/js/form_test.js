document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formulaire_test");
    const totalSections = 4;

    // Gérer l'affichage progressif des sections
    for (let i = 1; i <= totalSections; i++) {
        const section = document.getElementById("section" + i);
        const inputs = section.querySelectorAll("input[type='radio']");

        inputs.forEach(input => {
            input.addEventListener("change", () => {
                const answered = new Set();
                inputs.forEach(r => {
                    if (r.checked) {
                        answered.add(r.name);
                    }
                });

                if (answered.size === 5 && i < totalSections) {
                    document.getElementById("section" + (i + 1)).style.display = "block";
                }
            });
        });
    }

    // Gérer la soumission
    form.addEventListener("submit", (e) => {
        // Charger les données de la première partie depuis sessionStorage
        const partie1 = JSON.parse(sessionStorage.getItem("formulaire_partie1")) || {};

        // Ajouter dynamiquement les champs cachés de la partie 1
        Object.entries(partie1).forEach(([key, value]) => {
            const hidden = document.createElement("input");
            hidden.type = "hidden";
            hidden.name = key;
            hidden.value = String(value);
            form.appendChild(hidden);
            console.log("clé:", key, "→", "valeur:", value);
        });

        // Nettoyer sessionStorage (facultatif)
        sessionStorage.removeItem("formulaire_partie1");

    });
});
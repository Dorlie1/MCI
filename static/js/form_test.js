document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formulaire_test");
    const totalSections = 4;
    const formulaireDonUrl = document.getElementById("formulaire-container").dataset.formulaireDonUrl;

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
        e.preventDefault();

        const testData = {};
        for (let i = 1; i <= 21; i++) {
            const val = form.querySelector(`input[name="p${i}"]:checked`);
            if (val) testData[`p${i}`] = val.value;
        }
        sessionStorage.setItem("formulaire_partie2", JSON.stringify(testData));

        window.location.href = formulaireDonUrl;
    });
});
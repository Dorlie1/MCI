document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("password-form");
    const passwordEntre = document.getElementById("password");
    const error = document.getElementById("error");
    const formulaireInfoUrl = document.getElementById("formulaire-container").dataset.formulaireInfoUrl;

    const passwordsMensuels = [
        "Mci01", "Mci02", "Mci03", "Mci04",
        "Mci05", "Mci06", "Mci07", "Mci08",
        "Mci09", "Mci10", "Mci11", "Mci12"
    ];

    const moisCourant = new Date().getMonth(); // 0-11
    const passwordCourrant = passwordsMensuels[moisCourant];

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const passwordEntreUtilisateur = passwordEntre.value;

        if (passwordEntreUtilisateur === passwordCourrant) {
            window.location.href = formulaireInfoUrl;
        } else {
            error.textContent = "Mot de passe incorrect.";
            passwordEntre.value = "";
        }
    });
});
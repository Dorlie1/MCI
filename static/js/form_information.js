document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const courriel = document.getElementById("courriel");
    const courrielConfirm = document.getElementById("courriel_confirm");
    const prenom = document.getElementById("prenom");
    const nom = document.getElementById("nom");

    const salutOui = document.getElementById("date_salut_oui");
    const salutNon = document.getElementById("date_salut_non");
    const containerDateSalut = document.getElementById("date_salut");

    const baptiseOui = document.getElementById("baptise_oui");
    const baptiseNon = document.getElementById("baptise_non");
    const containerSouvenirDateBapteme = document.getElementById("souvenir_date_bapteme");
    const containerDateBapteme = document.getElementById("date_bapteme");
    const formulaireTestUrl = document.getElementById("formulaire-container").dataset.formulaireTestUrl;

    salutOui.addEventListener("change", () => {
        if (salutOui.checked) {
            containerDateSalut.innerHTML = `
                <label for="date_du_salut">Date de votre salut</label>
                <input type="date" id="date_du_salut" name="date_du_salut" required>
            `;
        }
    });

    salutNon.addEventListener("change", () => {
        containerDateSalut.innerHTML = "";
    });

    baptiseOui.addEventListener("change", () => {
        containerSouvenirDateBapteme.innerHTML = `
            <p>Vous souvenez-vous de la date de votre baptême ?</p>
            <div class="toggle-group">
                <input type="radio" id="souvenir_bapteme_oui" name="souvenir_bapteme" value="oui" required>
                <label for="souvenir_bapteme_oui" class="toggle toggle_oui">Oui</label>

                <input type="radio" id="souvenir_bapteme_non" name="souvenir_bapteme" value="non" checked required>
                <label for="souvenir_bapteme_non" class="toggle toggle_non">Non</label>
            </div>
        `;

        // Attache événements une fois le HTML injecté
        setTimeout(() => {
            const souvenirOui = document.getElementById("souvenir_bapteme_oui");
            const souvenirNon = document.getElementById("souvenir_bapteme_non");

            souvenirOui.addEventListener("change", () => {
                containerDateBapteme.innerHTML = `
                    <label for="date_du_bapteme">Date de votre baptême</label>
                    <input type="date" id="date_du_bapteme" name="date_du_bapteme" required>
                `;
            });

            souvenirNon.addEventListener("change", () => {
                containerDateBapteme.innerHTML = "";
            });
        }, 0);
    });

    baptiseNon.addEventListener("change", () => {
        containerSouvenirDateBapteme.innerHTML = "";
        containerDateBapteme.innerHTML = "";
    });

    // === Validation du formulaire
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const today = new Date().toISOString().split("T")[0];

        if (!emailRegex.test(courriel.value)) {
            alert("Veuillez entrer une adresse courriel valide.");
            courriel.focus();
            return;
        }

        if (courriel.value !== courrielConfirm.value) {
            alert("Les adresses courriel ne correspondent pas.");
            courrielConfirm.focus();
            return;
        }

        if (prenom.value.length > 100) {
            alert("Il y a une limite de 100 caractères pour le prénom.");
            prenom.focus();
            return;
        }

        if (nom.value.length > 100) {
            alert("Il y a une limite de 100 caractères pour le nom.");
            nom.focus();
            return;
        }

        const dateNaissance = document.getElementById("date_naissance");
        if (dateNaissance && dateNaissance.value > today) {
            alert("La date de naissance ne peut pas être dans le futur.");
            dateNaissance.focus();
            return;
        }

        const dateSalut = document.getElementById("date_du_salut");
        if (dateSalut && dateSalut.value > today) {
            alert("La date de salut ne peut pas être dans le futur.");
            dateSalut.focus();
            return;
        }

        const dateBapteme = document.getElementById("date_du_bapteme");
        if (dateBapteme && dateBapteme.value > today) {
            alert("La date de baptême ne peut pas être dans le futur.");
            dateBapteme.focus();
            return;
        }

        const etatMatrimonial = document.getElementById("etat_matrimonial");
        if (etatMatrimonial && etatMatrimonial.value === "nul") {
            alert("Veuillez sélectionner un état matrimonial valide.");
            etatMatrimonial.focus();
            return;
        }

        const data = {
            prenom: prenom.value,
            nom: nom.value,
            courriel: courriel.value,
            date_naissance: document.getElementById("date_naissance")?.value || "",
            genre: document.querySelector('input[name="genre"]:checked')?.value || "",
            date_salut: document.querySelector('input[name="date_salut"]:checked')?.value || "",
            date_du_salut: document.getElementById("date_du_salut")?.value || "",
            baptise: document.querySelector('input[name="baptise"]:checked')?.value || "",
            souvenir_bapteme: document.querySelector('input[name="souvenir_bapteme"]:checked')?.value || "",
            date_du_bapteme: document.getElementById("date_du_bapteme")?.value || "",
            etat_matrimonial: document.getElementById("etat_matrimonial").value,
            disponibilite: document.getElementById("disponibilite").value,
            precision: document.getElementById("precision").value,
        };

        sessionStorage.setItem("formulaire_partie1", JSON.stringify(data));

        window.location.href = formulaireTestUrl;
    });
});


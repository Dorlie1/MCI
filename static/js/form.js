document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form")
    const courriel = document.getElementById("courriel")
    const prenom = document.getElementById("prenom")
    const nom = document.getElementById("nom")
    const numero = document.getElementById("numero_telephone")
    const voiture = document.getElementById("voiture")
    const trim_oui = document.getElementById("peinture_trim_oui")
    const trim_non = document.getElementById("peinture_trim_non")
    const containerCouleur = document.getElementById("couleur")

    form.addEventListener("submit", function (e) {
        if (prenom.value.length > 100){
            e.preventDefault()
            alert("Il y a une limite de 100 charactères")
            prenom.focus();
        }
        if (nom.value.length > 100) {
            e.preventDefault()
            alert("Il y a une limite de 100 charactères")
            nom.focus();
        }
        if (numero.value.length > 20) {
            e.preventDefault()
            alert("Il y a une limite de 20 charactères")
            numero.focus();
        }
        if (voiture.value.length > 200) {
            e.preventDefault()
            alert("Il y a une limite de 200 charactères")
            voiture.focus();
        }
        if (trim_oui.checked) {
            couleur_trim = document.getElementById("couleur_trim")
            if (couleur_trim.value.length > 50) {
                e.preventDefault()
                alert("Il y a une limite de 50 charactères")
                couleur_trim.focus();
            }
        }
    })

    form.addEventListener("submit", function (e){
       const emailRegex =  /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
       if (!emailRegex.test(courriel.value)) {
           e.preventDefault()
           alert("Veuillez entrer une adresse courriel valide.");
           courriel.focus();
       }
    });

    trim_oui.addEventListener("change", function () {
        if(trim_oui.checked) {
            injecteCouleur();
        }
    });

    trim_non.addEventListener("change", function () {
        if(trim_non.checked) {
            containerCouleur.innerHTML = "";
        }
    });

    function injecteCouleur() {
        containerCouleur.innerHTML = `
            <label for="nom">Quelle couleur est desirée ?</label>
            <input type="text" id="couleur_trim" name="couleur_trim" required>
        `;
    }
});
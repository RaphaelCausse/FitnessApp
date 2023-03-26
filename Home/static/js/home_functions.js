window.onload = function additionner() {
    // Obtenir les valeurs des balises d'entrée
    let valeur1 = parseInt(document.getElementById("objectif-val").innerText);
    let valeur2 = parseInt(document.getElementById("sport-val").innerText);
    let valeur3 = parseInt(document.getElementById("alim-val").innerText);
    
    // Additionner les valeurs
    let resultat = valeur1 + valeur2 - valeur3;
    
    // Afficher le résultat dans la balise de sortie
    document.getElementById("rest-val").innerHTML = resultat;
  }
  
-- Création de la table utilisateur (un seul utilisateur permis)
CREATE TABLE utilisateur (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    nom TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL
);

-- Création de la table roles
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texte TEXT NOT NULL
);

INSERT INTO utilisateur (id, nom, mot_de_passe)
VALUES (1, 'Admin', 'a02f0b3c1fae2b176861f7eac4f8ab8d0c5b0b69cd342729ff95e25b8b0aa624');
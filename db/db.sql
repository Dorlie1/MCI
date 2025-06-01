-- Création de la table utilisateur (un seul utilisateur permis)
CREATE TABLE utilisateur (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    nom TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL
);

-- Création de la table regions
CREATE TABLE regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

-- Création de la table traits
CREATE TABLE traits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Création de la table roles
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    trait_id INTEGER NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (trait_id) REFERENCES traits(id)
);

-- Insertion de l'utilisateur par défaut avec le nouveau mot de passe (123456theof)
INSERT INTO utilisateur (id, nom, mot_de_passe)
VALUES (1, 'Admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');

-- Insertion des régions
INSERT INTO regions (nom) VALUES 
('Montreal'),
('Saint-Bruno');

-- Insertion des traits
INSERT INTO traits (code, description) VALUES 
('D', 'Dominance'),
('I', 'Influence'),
('S', 'Stabilité'),
('C', 'Conformité');

-- Insertion des roles pour Montreal
INSERT INTO roles (nom, region_id, trait_id) VALUES 
-- Dominance (D)
('Coordonnateurs de scène', 1, 1),
('Louange - Bass', 1, 1),
('Louange - Piano', 1, 1),
('Louange - Guitar', 1, 1),
('Louange - Saxophone', 1, 1),
('Théâtre', 1, 1),

-- Influence (I)
('Baptême', 1, 2),
('Portier', 1, 2),
('Église Enfant', 1, 2),
('Accompagnateur', 1, 2),
('Valet', 1, 2),
('Hospitalité', 1, 2),
('Salon équipe créative', 1, 2),
('Parcours Découverte (Accueil)', 1, 2),
('Accueil', 1, 2),

-- Stabilité (S)
('Banque Alimentaire', 1, 3),
('Prière', 1, 3),
('Assiste le Leader de petits groupes', 1, 3),
('Église Enfant', 1, 3),
('Hospitalité', 1, 3),
('Accompagnateur', 1, 3),

-- Conformité (C)
('Logistique événementiel', 1, 4),
('Église enfant', 1, 4),
('Banque alimentaire', 1, 4),
('Portier', 1, 4),
('Valet', 1, 4),
('Aide Décoration de Noel', 1, 4);

-- Insertion des roles pour Saint-Bruno
INSERT INTO roles (nom, region_id, trait_id) VALUES 
-- Dominance (D)
('Coordonnateurs de scène', 2, 1),
('Louange - Bass', 2, 1),
('Louange - Piano', 2, 1),
('Louange - Guitar', 2, 1),
('Louange - Saxophone', 2, 1),

-- Influence (I)
('Baptême', 2, 2),
('Portier', 2, 2),
('Église Enfant', 2, 2),
('Accompagnateur', 2, 2),
('Valet', 2, 2),
('Hospitalité', 2, 2),
('Salon équipe créative', 2, 2),
('Parcours Découverte (Accueil)', 2, 2),
('Accueil', 2, 2),

-- Stabilité (S)
('Hospitalité pour la prière', 2, 3),
('Hospitalité', 2, 3),
('Comptoir Check in', 2, 3),
('Équipe des Volontaires', 2, 3),
('Baptême', 2, 3),
('Parcours Découverte (Accueil)', 2, 3),
('Portier', 2, 3),

-- Conformité (C)
('Logistique événementiel', 2, 4),
('Église enfant', 2, 4),
('Banque alimentaire', 2, 4),
('Portier', 2, 4),
('Valet', 2, 4),
('Aide Décoration de Noel', 2, 4),
('Parcours découverte (aide à placer les matériels)', 2, 4);
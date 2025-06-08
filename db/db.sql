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
CREATE TABLE dons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,         -- 'A', 'B', ..., 'N'
    nom TEXT NOT NULL,          -- e.g., "Administration"
    description TEXT NOT NULL   -- Description of the don
);

-- Création de la table roles
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    don_id INTEGER NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (don_id) REFERENCES dons(id)
);

-- Insertion de l'utilisateur par défaut avec le nouveau mot de passe (123456theof)
INSERT INTO utilisateur (id, nom, mot_de_passe)
VALUES (1, 'Admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');

-- Insertion des régions
INSERT INTO regions (nom) VALUES 
('Montreal'),
('Saint-Bruno');

-- Insertion des dons
INSERT INTO dons (code, nom, description) VALUES
('A', 'Administration', 'Le don d’administration est la force ou habileté divine d’organiser de multiples tâches et groupes de personnes pour accomplir ces tâches. Luc 14 : 28-30; Actes 6 :1-7; 1 Corinthiens 12 :28'),
('B', 'Counseling', 'Le don de counseling est la capacité divine de dépéndre du l’œuvre du St-Esprit pour donner la direction de Dieu et non la nôtre – bonne communication, bon écouteur.'),
('C', 'Habileté Manuelle', 'Le don d’habileté manuelle est la force ou habileté divine de planifier, construire et travailler de vos mains dans des environnements de construction pour accomplir de multiples applications ministérielles. Exode 30 : 22, 31 : 3-11; 2 Chroniques 34 : 9-13; Actes 18 : 2-3'),
('D', 'Musique/Louange', 'Le don de communication créative est la force ou habileté divine de chanter, danser, ou jouer un instrument dans le but, principalement, d’aider les autres à louer Dieu. Deutéronome 31 : 22 1 Samuel 16 : 16, 1 Chroniques 16 : 41-42 2 Chroniques 5 : 12-13, 34 : 12 Psaume 150'),
('E', 'Exhortation', 'Le don d’exhortation est la force ou habileté divine d’encourager les autres par le moyen de la parole écrite ou verbale et par les vérités bibliques. Actes 14 : 22, Romains 12 : 8, 1 Timothée 4 : 13, Hébreux 10 : 24-25'),
('F', 'Évangélisme', 'Le don d’évangélisme est la force ou habileté divine d’aider les non chrétiens à faire les pas nécessaires pour devenir disciples de Christ. Actes 8 : 5-6 8 : 26-40 14 : 21, 21 : 8, Éphésiens 4 : 11-14'),
('G', 'Libéralité', 'Le don de libéralité est la force ou habileté divine de créer de la richesse et de donner au moyen des dîmes et des offrandes dans le but de faire avancer le royaume de Dieu sur la terre. Marc 12 : 41-44, Romains 12 : 8, 2 Corinthiens 8 : 1-7, 9 : 2-7'),
('H', 'Aide', 'Le don d’aide est la force ou habileté divine de travailler dans un rôle de support pour l’accomplissement de tâches dans le ministère chrétien. Marc 15 : 40-41 Actes 9 :36 Romains 16 :1-2 1 Corinthiens 12 :28'),
('I', 'Hospitalité', 'Le don d’hospitalité est la force ou habileté divine de créer un environnement chaleureux et invitant pour les autres, dans des lieux tels qu’à la maison, au bureau ou à l’église. Actes 16 : 14-15 Romains 12 : 13, 16 :23 Hébreux 13 : 1-2 1 Pierre 4 : 9'),
('J', 'Leadership', 'Le don de leadership est la force ou habileté divine d’influencer les gens à leur niveau tout en les dirigeant et les focalisant sur l’image globale, la vision ou l’idée. Romains 12 : 8 1 Timothée 3 : 1-13, 5 :17 Hébreux 13 : 17'),
('K', 'Miséricorde', 'Le don de miséricorde est la force ou habileté divine de ressentir de l’empathie et d’être concerné pour ceux qui souffrent, quelle que soit la façon. Matthieu 9 : 35-36 Marc 9 : 41 Romains 12 : 8 1 Thessaloniciens 5 :14'),
('L', 'Prophète', 'Le don de prophète est la force ou habileté divine de parler hardiment et clarifier des vérités scripturales et doctrinales, dans certains cas, annonçant à l’avance le plan de Dieu. Actes 2 : 37-40, 7 : 51-53, 26 : 24-29 1 Corinthiens 14 : 1-4 1 Thessaloniciens 1 :5'),
('M', 'Berger', 'Le don de berger est la force ou habileté divine d’être concerné pour les besoins personnels des autres en prenant soin et améliorant les situations problématiques de la vie. Jean 10 : 1-18 Éphésiens 4 : 11-14 1 Timothée 3 : 1-7 1 Pierre 5 : 1-3'),
('N', 'Enseignement', 'Le don d’enseignement est la force ou habileté divine d’étudier et d’apprendre des Écritures, principalement pour apporter la compréhension et la croissance aux autres chrétiens. Actes 18 : 24-28, 20 : 20-21 1 Corinthiens 12 : 28 Éphésiens 4 : 11-14');

-- Insertion des roles
-- Montreal (region_id = 1)
INSERT INTO roles (nom, region_id, don_id) VALUES
('Évènementiel', 1, 1), ('Placer (Entrée de données)', 1, 1), ('Réseaux sociaux', 1, 1), ('Baptême', 1, 1), ('Traduction', 1, 1), ('Comptoir check-In', 1, 1),
('Accompagnateur', 1, 2), ('Hospitalité pour la prière', 1, 2), ('Hospitalité', 1, 2), ('Comptoir Check in', 1, 2), ('Équipe des Volontaires', 1, 2), ('Baptême', 1, 2), ('Portier', 1, 2),
('Logistique événementiel', 1, 3), ('Église enfant', 1, 3), ('Banque alimentaire', 1, 3), ('Portier', 1, 3), ('Valet', 1, 3), ('Aide Décoration de Noel', 1, 3),
('Coordonnateurs de scène', 1, 4), ('Louange (Musicien: Basse, pianiste, guitariste, saxophoniste)', 1, 4), ('Théâtre', 1, 4),
('Accompagnateur', 1, 5), ('Hospitalité pour la prière', 1, 5), ('Hospitalité', 1, 5), ('Comptoir Check in', 1, 5), ('Équipe des Volontaires', 1, 5), ('Baptême', 1, 5), ('Portier', 1, 5),
('Assister le leader de petits groupes (évangélisation)', 1, 6), ('Accompagnateurs', 1, 6),
('Panier d’offrande', 1, 7), ('Banque Alimentaire', 1, 7),
('Placer', 1, 8), ('Réseaux sociaux', 1, 8), ('Portier', 1, 8), ('Moniteur Église enfant', 1, 8), ('Comptoir Check in', 1, 8), ('Logistique événementiel', 1, 8), ('Salon équipe créative', 1, 8), ('Baptême', 1, 8), ('Banque Alimentaire', 1, 8), ('Entretien', 1, 8), ('Traduction', 1, 8),
('Baptême', 1, 9), ('Portier', 1, 9), ('Église Enfant', 1, 9), ('Accompagnateur', 1, 9), ('Valet', 1, 9), ('Hospitalité', 1, 9), ('Salon équipe créative', 1, 9), ('Parcours Découverte (Accueil)', 1, 9), ('Accueil', 1, 9),
('Assiter le leader de petits groupes', 1, 10), ('Toutes les équipes', 1, 10),
('Banque Alimentaire', 1, 11), ('Prière', 1, 11),
('Prière', 1, 12), ('Assiste le Leader de petits groupes', 1, 12),
('Église Enfant', 1, 13), ('Assiste le leader de petits groupes (appel pour soin)', 1, 13), ('Hospitalité', 1, 13), ('Accompagnateur', 1, 13),
('Assiste le leader de petits groupes', 1, 14), ('Parcours Découverte', 1, 14);

-- Saint-Bruno (region_id = 2)
INSERT INTO roles (nom, region_id, don_id) VALUES
('Évènementiel', 2, 1), ('Coordonnateurs de scène', 2, 1), ('Coordonnateurs de plancher', 2, 1), ('Hospitalité', 2, 1), ('Hospitalité pour la prière', 2, 1), ('Équipe des Volontaires', 2, 1), ('Valet', 2, 1), ('Traduction', 2, 1), ('Parcours Découverte', 2, 1),
('Accompagnateur', 2, 2), ('Hospitalité pour la prière', 2, 2), ('Hospitalité', 2, 2), ('Comptoir Check in', 2, 2), ('Équipe des Volontaires', 2, 2), ('Baptême', 2, 2), ('Parcours Découverte (Accueil)', 2, 2), ('Portier', 2, 2),
('Logistique événementiel', 2, 3), ('Église enfant', 2, 3), ('Banque alimentaire', 2, 3), ('Portier', 2, 3), ('Valet', 2, 3), ('Aide Décoration de Noel', 2, 3), ('Parcours découverte (aide à placer les matériels)', 2, 3),
('Coordonnateurs de scène', 2, 4), ('Louange (Musicien: Basse, pianiste, guitariste, saxophoniste)', 2, 4),
('Accompagnateur', 2, 5), ('Hospitalité pour la prière', 2, 5), ('Hospitalité', 2, 5), ('Comptoir Check in', 2, 5), ('Équipe des Volontaires', 2, 5), ('Baptême', 2, 5), ('Parcours Découverte (Accueil)', 2, 5), ('Portier', 2, 5),
('Assister le leader de petits groupes (évangélisation)', 2, 6), ('Accompagnateurs', 2, 6),
('Panier d’offrande', 2, 7),
('Coordonnateurs de scène', 2, 8), ('Coordonnateurs de plancher', 2, 8), ('Logistique', 2, 8), ('Moniteurs (église enfant)', 2, 8), ('Hospitalité', 2, 8), ('Hospitalité pour la prière', 2, 8), ('Parcours découverte', 2, 8), ('Traduction', 2, 8), ('Valet', 2, 8), ('Équipe des Volontaires', 2, 8),
('Baptême', 2, 9), ('Portier', 2, 9), ('Église Enfant', 2, 9), ('Accompagnateur', 2, 9), ('Valet', 2, 9), ('Hospitalité', 2, 9), ('Salon équipe créative', 2, 9), ('Parcours Découverte (Accueil)', 2, 9), ('Accueil', 2, 9),
('Assister le leader de petits groupes', 2, 10), ('Toutes les équipes', 2, 10),
('Prière', 2, 11),
('Prière', 2, 12), ('Assiste le Leader de petits groupes', 2, 12),
('Église Enfant', 2, 13), ('Assiste Leader de petits groupes (appel pour soin)', 2, 13), ('Hospitalité', 2, 13), ('Accompagnateur', 2, 13),
('Assiste le leader de petits groupes', 2, 14), ('Parcours Découverte', 2, 14);
-- Schéma de base de données pour l'application de gestion de stock Succès Fuel
-- Adapté pour PostgreSQL

-- Table des profils
CREATE TABLE profil (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    libelle VARCHAR(100) NOT NULL
);

-- Table des compagnies pétrolières
CREATE TABLE compagnie_petrolier (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des marques de compagnie
CREATE TABLE marque_compagnie (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    compagnie_petrolier_id INTEGER NOT NULL,
    FOREIGN KEY (compagnie_petrolier_id) REFERENCES compagnie_petrolier(id)
);

-- Table des utilisateurs
CREATE TABLE utilisateur (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    login VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    profil_id INTEGER NOT NULL,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profil_id) REFERENCES profil(id)
);

-- Table des stations
CREATE TABLE station (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    informations JSONB,

    compagnie_petrolier_id INTEGER NOT NULL,
    marque_id INTEGER NOT NULL,

    utilisateur_id INTEGER NOT NULL, -- gérant de la station

    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (compagnie_petrolier_id) REFERENCES compagnie_petrolier(id),
    FOREIGN KEY (marque_id) REFERENCES marque_compagnie(id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);

-- Table des produits
CREATE TABLE produit (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    libelle VARCHAR(100) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('CARBURANT', 'LUBRIFIANT')) NOT NULL,
    actif BOOLEAN DEFAULT TRUE
);

-- Table des cuves
CREATE TABLE cuve (
    id SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL,
    produit_id INTEGER NOT NULL,
    capacite DECIMAL(15,3) NOT NULL,
    barremage JSONB NOT NULL,
    actif BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (station_id) REFERENCES station(id),
    FOREIGN KEY (produit_id) REFERENCES produit(id)
);

-- Table des pistolets
CREATE TABLE pistolet (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50),
    cuve_id INTEGER NOT NULL,
    actif BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (cuve_id) REFERENCES cuve(id)
);

-- Table des mouvements de stock
CREATE TABLE mouvement_stock (
    id BIGSERIAL PRIMARY KEY,

    station_id INTEGER NOT NULL,
    produit_id INTEGER NOT NULL,
    cuve_id INTEGER,

    type_mouvement VARCHAR(20) CHECK (type_mouvement IN ('ACHAT', 'VENTE', 'INVENTAIRE')) NOT NULL,
    quantite DECIMAL(15,3) NOT NULL,
    date_mouvement TIMESTAMP NOT NULL,

    utilisateur_id INTEGER NOT NULL,
    infos JSONB,

    FOREIGN KEY (station_id) REFERENCES station(id),
    FOREIGN KEY (produit_id) REFERENCES produit(id),
    FOREIGN KEY (cuve_id) REFERENCES cuve(id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);

-- Table des stocks par station
CREATE TABLE stock_station (
    station_id INTEGER NOT NULL,
    produit_id INTEGER NOT NULL,
    quantite DECIMAL(15,3) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (station_id, produit_id),
    FOREIGN KEY (station_id) REFERENCES station(id),
    FOREIGN KEY (produit_id) REFERENCES produit(id)
);

-- Index pour améliorer les performances
CREATE INDEX idx_mouvement_stock_date ON mouvement_stock(date_mouvement);
CREATE INDEX idx_mouvement_stock_station ON mouvement_stock(station_id);
CREATE INDEX idx_mouvement_stock_produit ON mouvement_stock(produit_id);



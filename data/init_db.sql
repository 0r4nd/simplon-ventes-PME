
CREATE TABLE magasins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_magasin INT,
  nom_ville TEXT,
  nombre_salaries INT
);

CREATE TABLE produits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nom TEXT,
  id_ref_produit TEXT,
  prix FLOAT,
  stock INT
);

CREATE TABLE ventes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE,
  id_ref_produit TEXT,
  quantite INT,
  id_magasin INT
);

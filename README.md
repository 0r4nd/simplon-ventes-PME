# Simplon-ventes-PME
[Objectifs visés:](brief/Brief%20projet%20Analyser%20les%20ventes%20d’une%20PME%20-%20Data%20Engineer%20-%20V2.pdf)
- Créer et mettre en œuvre un environnement à deux services : un pour l’exécution des scripts (import de données) et un autre pour la base de données
- Analyser un jeu de données et en expliquer ses caractéristiques
- Créer une base de données adaptée pour le stockage du jeu de données
- Importer les données
- Réaliser un premier niveau d’analyses de données avec SQL
- Stocker les résultats des analyses.
<br>

# Livrables:

## ● Le schéma de l’architecture conçu
à ajouter (pour le moment il n'y a qu'un service qui fait la conversion des données au démarrage, puis renvois un json spécifique aux 3 requêtes)
<br>

## ● Le schéma des données (sous une forme standard, MCD par exemple)
<div style="text-align:center">
  <img src="schema_tables.png" width="600">
</div>
<br>

## ● Le Dockerfile
[Dockerfile](Dockerfile)
<br>

## ● Le fichier yaml du Docker Compose
à ajouter (pour le moment il n'y a qu'un service qui fait la conversion des données au démarrage, puis renvois un json spécifique aux 3 requêtes)
<br>

## ● Le(s) script(s) d'exécution pour la collecte, transformation, et import des données
- Script final: [simplon_vente_pme/api/fast.py](simplon_vente_pme/api/fast.py)
- Document de travail: [notebooks/simplon-ventes-PME.ipynb](notebooks/simplon-ventes-PME.ipynb)
<br>

## ● Le fichier sql
[datasets/table.sqlite](datasets/table.sqlite)
<br>

## ● Une note rappelant les résultats d’analyse obtenus (point 4.a, 4.b, 4.c).
- 4.a requête pour obtenir le chiffre d'affaires total

avec docker en local: http://127.0.0.1:8000/total_sales
```sql
SELECT SUM(ventes.quantite*produits.prix) AS prix_total 
FROM ventes
LEFT JOIN produits ON ventes.id_ref_produit = produits.id_ref_produit
```
|   | prix_total |
| - | ------------- |
| 1 | 5268.78 |
<br>

- 4.b requête pour obtenir les ventes par produit

avec docker en local: http://127.0.0.1:8000/sales_by_product
```sql
SELECT produits.nom,
       SUM(ventes.quantite) AS nombre_ventes,
       produits.prix AS prix_unitaire,
       SUM(ventes.quantite)*produits.prix AS prix_total
FROM produits
LEFT JOIN ventes ON (ventes.id_ref_produit = produits.id_ref_produit)
GROUP BY produits.nom
```
|   | nom | nombre_ventes | prix_unitaire | prix_total |
| - | ------------- | ------------- | ------------- | ------------- |
| 1 | Produit A | 24 | 49.99 | 1199.76 |
| 2 | Produit B | 27 | 19.99 | 539.73 |
| 3 | Produit C | 15 | 29.99 | 449.85 |
| 4 | Produit D | 21 | 79.99 | 1679.79 |
| 5 | Produit E | 35 | 39.99 | 1399.65 |
<br>

- 4.c requête pour obtenir les ventes par région

avec docker en local: http://127.0.0.1:8000/sales_by_region
```sql
SELECT magasins.nom_ville,
       SUM(ventes.quantite) AS nombre_ventes
FROM magasins
LEFT JOIN ventes ON (magasins.id_magasin = ventes.id_magasin)
GROUP BY nom_ville
ORDER BY nombre_ventes DESC
```
|   | nom | nombre_ventes |
| - | ------------- | ------------- |
| 1 | Marseille | 27 |
| 2 | Lyon | 21 |
| 3 | Paris | 20 |
| 4 | Bordeaux | 19 |
| 5 | Nantes | 17 |
| 6 | Strasbourg | 11 |
| 7 | Lille | 7 |
<br>


# Utils
Launch api with uvicorn:
```sh
  uvicorn simplon_vente_pme.api.fast:app --reload
```
<br><br>

Add project to env variables
```sh
GAR_IMAGE=simplon_vente_pme
```

Build docker image:
```sh
  docker build --tag=$GAR_IMAGE:dev .
```

Run docker image:
```sh
  docker run -it -e PORT=8000 -p 8000:8000 $GAR_IMAGE:dev
```



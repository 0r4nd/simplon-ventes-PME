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
<br>

## ● Le schéma des données (sous une forme standard, MCD par exemple)
<div style="text-align:center">
  <img src="schema_tables.png" width="600">
</div>
<br>

## ● Le Dockerfile
<br>

## ● Le fichier yaml du Docker Compose
<br>

## ● Le(s) script(s) d'exécution pour la collecte, transformation, et import des données
- Script final: [api/fast.py](api/fast.py)
- Document de travail: [notebooks/simplon-ventes-PME.ipynb](notebooks/simplon-ventes-PME.ipynb)
<br>

## ● Le fichier sql
[datasets/table.sqlite](datasets/table.sqlite)
<br>

## ● Une note rappelant les résultats d’analyse obtenus (point 4.a, 4.b, 4.c).
- 4.a requête pour obtenir le chiffre d'affaires total
```sql
SELECT SUM(ventes.quantite*produits.prix) AS prix_ventes_total 
FROM ventes
LEFT JOIN produits ON ventes.id_ref_produit = produits.id_ref_produit
```
|   | prix_ventes_total |
| - | ------------- |
| 1 | 5268.78 |
<br>

- 4.b requête pour obtenir les ventes par produit
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
<br>

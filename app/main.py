

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# misc
import os
import requests
from io import StringIO

# load/save files
import sqlite3

# datascience libs
import pandas as pd

db_filename = "db.sqlite"
path_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def insert_items_to_magasin(name_table, path="", list_id_magasin=[], list_nom_villes=[], list_salaries=[]):
    path_table = os.path.join(path, name_table)
    if not os.path.exists(path_table):
        return
    if len(list_id_magasin) == 0:
        return

    with sqlite3.connect(path_table) as conn:
        cursor = conn.cursor()

    for i in range(len(list_id_magasin)):
        query = """
            INSERT INTO magasins (id_magasin, nom_ville, nombre_salaries)
            SELECT
                T.*
            FROM
                (SELECT {} id_magasin, '{}' nom_ville, {} nombre_salaries) T
                    LEFT JOIN
                magasins ON magasins.id_magasin = T.id_magasin AND magasins.nom_ville = T.nom_ville
            WHERE
                magasins.id_magasin is null
            """.format(list_id_magasin[i], list_nom_villes[i], list_salaries[i])

        cursor.execute(query)
        conn.commit()

    conn.close()


def insert_items_to_produits(name_table, path="", list_nom=[], list_id_ref_produit=[], list_prix=[], list_stock=[]):
    path_table = os.path.join(path, name_table)
    if not os.path.exists(path_table):
        return
    if len(list_nom) == 0:
        return

    with sqlite3.connect(path_table) as conn:
        cursor = conn.cursor()

    for i in range(len(list_nom)):
        query = """
            INSERT INTO produits (nom, id_ref_produit, prix, stock)
            SELECT
                T.*
            FROM
                (SELECT '{}' nom, '{}' id_ref_produit, {} prix, {} stock) T
                    LEFT JOIN
                produits ON produits.nom = T.nom AND produits.id_ref_produit = T.id_ref_produit
            WHERE
                produits.nom IS null
            """.format(list_nom[i], list_id_ref_produit[i], list_prix[i], list_stock[i])

        cursor.execute(query)
        conn.commit()

    conn.close()


def insert_items_to_ventes(name_table, path="", list_date=[], list_id_ref_produit=[], list_quantite=[], list_id_magasin=[]):
    path_table = os.path.join(path, name_table)
    if not os.path.exists(path_table):
        return
    if len(list_date) == 0:
        return

    with sqlite3.connect(path_table) as conn:
        cursor = conn.cursor()

    for i in range(len(list_date)):
        query = """
            INSERT INTO ventes (date, id_ref_produit, quantite, id_magasin)
            SELECT
                T.*
            FROM
                (SELECT '{}' date, '{}' id_ref_produit, {} quantite, {} id_magasin) T
                    LEFT JOIN
                ventes ON ventes.date = T.date AND ventes.id_ref_produit = T.id_ref_produit AND ventes.id_magasin = T.id_magasin
            WHERE
                ventes.date IS null
            """.format(list_date[i], list_id_ref_produit[i], list_quantite[i], list_id_magasin[i])

        cursor.execute(query)
        conn.commit()

    conn.close()


def convert_csv_to_sqlite(db_name = db_filename):
    path_datasets = os.path.join(path_, "data")

    # from files
    #df_magasins = pd.read_csv(os.path.join(path_datasets, "magasins.csv"))
    #df_produits = pd.read_csv(os.path.join(path_datasets, "produits.csv"))
    #df_ventes = pd.read_csv(os.path.join(path_datasets, "ventes.csv"))

    # from HTTP
    res = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv")
    res.encoding = "utf-8"
    df_ventes = pd.read_csv(StringIO(res.text))

    res = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv")
    res.encoding = "utf-8"
    df_produits = pd.read_csv(StringIO(res.text))

    res = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv")
    res.encoding = "utf-8"
    df_magasins = pd.read_csv(StringIO(res.text))

    insert_items_to_magasin(db_name, path_datasets,
                            df_magasins['ID Magasin'].values.tolist(),
                            df_magasins['Ville'].values.tolist(),
                            df_magasins['Nombre de salariés'].values.tolist())

    insert_items_to_produits(db_name, path_datasets,
                            df_produits['Nom'].values.tolist(),
                            df_produits['ID Référence produit'].values.tolist(),
                            df_produits['Prix'].values.tolist(),
                            df_produits['Stock'].values.tolist())

    insert_items_to_ventes(db_name, path_datasets,
                            df_ventes['Date'].values.tolist(),
                            df_ventes['ID Référence produit'].values.tolist(),
                            df_ventes['Quantité'].values.tolist(),
                            df_ventes['ID Magasin'].values.tolist())


# utils
def dict_fetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    convert_csv_to_sqlite(db_filename)
    return {"Hello": "World"}


@app.get("/total_sales")
def total_sales():
    path_table = os.path.join(os.path.join(path_, "data"), db_filename)

    with sqlite3.connect(path_table) as conn:
        cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(ventes.quantite*produits.prix) AS prix_total
        FROM ventes
        LEFT JOIN produits ON ventes.id_ref_produit = produits.id_ref_produit
        """)
    response = round(cursor.fetchone()[0], 3)
    conn.close()
    return response


@app.get("/sales_by_product")
def sales_by_product():
    path_table = os.path.join(os.path.join(path_, "data"), db_filename)

    with sqlite3.connect(path_table) as conn:
        cursor = conn.cursor()

    cursor.execute("""
        SELECT produits.nom,
            SUM(ventes.quantite) AS nombre_ventes
        FROM produits
        LEFT JOIN ventes ON (ventes.id_ref_produit = produits.id_ref_produit)
        GROUP BY produits.nom
        """)
    response = dict_fetchall(cursor)
    conn.close()
    return response


@app.get("/sales_by_region")
def sales_by_region():
    path_table = os.path.join(os.path.join(path_, "data"), db_filename)

    with sqlite3.connect(path_table) as conn:
        cursor = conn.cursor()

    cursor.execute("""
        SELECT magasins.nom_ville,
            SUM(ventes.quantite) AS nombre_ventes
        FROM magasins
        LEFT JOIN ventes ON (magasins.id_magasin = ventes.id_magasin)
        GROUP BY nom_ville
        ORDER BY nombre_ventes DESC
        """)
    response = dict_fetchall(cursor)
    conn.close()
    return response

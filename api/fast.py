

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# misc
import os
from timeit import default_timer as timer
from datetime import datetime

# load/save files
import sqlite3

# plot
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

# datascience libs
import pandas as pd


try: # python
    path_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
except NameError: # jupyter notebook
    path_ = os.path.dirname(os.getcwd())


def create_table(name_table, path="", remove_if_exist=False):
    path_table = os.path.join(path, name_table)
    if os.path.exists(path_table):
        if remove_if_exist:
            os.remove(path_table)
        else:
            return

    with sqlite3.connect(path_table) as conn:
        cursor = conn.cursor()

    # magasins
    cursor.execute(
        "CREATE TABLE magasins (id INTEGER PRIMARY KEY AUTOINCREMENT, id_magasin INT, nom_ville TEXT, nombre_salaries INT)")
    # produits
    cursor.execute(
        "CREATE TABLE produits (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, id_ref_produit TEXT, prix FLOAT, stock INT)")
    # ventes
    cursor.execute(
        "CREATE TABLE ventes (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, id_ref_produit TEXT, quantite INT, id_magasin INT)")

    conn.commit()
    conn.close()


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


def convert_csv_to_sqlite(db_name = "table.sqlite"):
    path_datasets = os.path.join(path_, "datasets")
    df_magasins = pd.read_csv(os.path.join(path_datasets, "magasins.csv"))
    df_produits = pd.read_csv(os.path.join(path_datasets, "produits.csv"))
    df_ventes = pd.read_csv(os.path.join(path_datasets, "ventes.csv"))

    create_table(db_name, path_datasets, True)

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


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup: create table from csv
    convert_csv_to_sqlite("table.sqlite")
    yield
    # on shutdown


@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/total_sales")
def total_sales():
    response = {
        "sales": round(5.56565656, 3),
    }
    return response

@app.get("/sales_by_product")
def sales_by_product(product):
    response = {
        "product": product,
        "sales_count": 50,
    }
    return response

@app.get("/sales_by_region")
def sales_by_region(region):
    response = {
        "region": region,
        "sales_count": 50,
    }
    return response

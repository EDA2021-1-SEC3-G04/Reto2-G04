﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 * 
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time 
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo de videos del modelo.
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos del archivo en la estrucura de datos
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadVideos(catalog)
    loadCategoryIds(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory
    
def loadVideos(catalog):
    """
    Carga los videos del archivo.  
    Por cada video se toma su categoria y su pais y por cada uno de estos se crea un lista, donde se guardan los videos correspondientes a esa categoria/pais
    """
    videosFiles = cf.data_dir + "Videos/videos-large.csv"
    input_file = csv.DictReader(open(videosFiles, encoding="utf-8"))
    for video in input_file:
        model.addVideo(catalog, video)


def loadCategoryIds(catalog):
    """
    Carga todos los category ids del archivo y los agrega a la lista de category ids
    """
    categoriesFiles = cf.data_dir + "Videos/category-id.csv"
    input_file = csv.DictReader(
        open(categoriesFiles, encoding="utf-8"), delimiter='\t')
    for category in input_file:
        model.addCategory(catalog, category)

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento
def sortViews(views_list):
    """
    Ordena los libros por views
    """
    return model.sortViews(views_list)

# Funciones de consulta sobre el catálogo

def getCategoryId(catalog, category):
    """
    Retorna la informacion de esa categoria: lista de videos correspondientes
    """
    return model.getCategoryId(catalog, category)

def getCategory(catalog, category_id): 
    return model.getCategory(catalog, category_id)

def topCountryCategory(catalog, number, country, category_id): 
    """
    Función base requerimiento 1. 
    Retorna lista con los top x videos con más views de un pais y una categoria
    """
    category_list = getCategory(catalog, category_id)
    sorted_cat_list = sortViews(category_list['videos'])
    top_vids = findTopsCountryCategory(sorted_cat_list, number, country)
    return top_vids


def videoSize(catalog):
    """
    Numero de videos cargados al catalogo
    """
    return model.videoSize(catalog)

def categorySize(catalog):
    """
    Numero de videos cargados al catalogo
    """
    return model.videoSize(catalog)


def findTopsCountryCategory(sorted_cat_list, number, country): 
    """
    Llama a funcion del modelo que busca y retorna los x videos con más views que son del 
    pais correspondiente
    """
    return model.findTopsCountryCategory(sorted_cat_list, number, country)

# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory


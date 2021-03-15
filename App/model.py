"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS122 5 - Estructuras de Datos y Algoritmos
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newCatalog():
    """
    Se define la estructura de un catálogo de videos. El catálogo tendrá tres 4, una para los videos, una para los category ids, otra para las categorias de los mismos y otra para los paises de los mismos.
    """
    catalog = {'videos': None,
               'by_countries': None,
               'by_categories': None,
               'category-id': None,
               'video-id': None}

    catalog['videos'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpVideoIdsLt)
    catalog['by_categories'] = mp.newMap(390000, maptype='CHAINING', loadfactor=4.0, comparefunction=cmpVideoCategories)
    catalog['category-id'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['video-id'] = mp.newMap(390000, maptype='CHAINING', loadfactor=4.0, comparefunction=cmpVideoIds)
    return catalog

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    """
    Se añade un video a a lista de videos
    """
    lt.addLast(catalog['videos'], video)
    mp.put(catalog['video-id'], video["video_id"], video)
    #country = video['country'].strip()
    # Funciones para añadir datos a las listas de pais y categoria
    #addVideoCountry(catalog, country, video)
    addVideoCategory(catalog, video)


def addCategory(catalog, category):
    """
    Se añade una categoria (su id y nombre) a a lista de categoria
    """
    c = newCategoryId(category['id'], category['name'])
    lt.addLast(catalog['category-id'], c)


def addVideoCountry(catalog, country, video):
    """
    Adiciona un pais a lista de paises.
    Las listas de cada pais guarda referencias a los videos de dicho pais
    """
    countries_list = catalog['by_countries']
    posCountry = lt.isPresent(countries_list, country)

    if posCountry > 0:  # El pais ya ha sido creada dentro de la lista
        new_country = lt.getElement(countries_list, posCountry)
    else:   # Debemos crear nuevo pais
        new_country = newCountry(country)
        lt.addLast(countries_list, new_country)
    lt.addLast(new_country['videos'], video)

def addVideoCategory(catalog, video):
    """
    Adiciona una categoria a lista de categorias si este no esta.
    Las listas de cada pais guarda referencias a los videos de dicho pais
    """
    try: 
        categories = catalog['by_categories']
        if video['category_id'] != '': 
            category_id = int(video['category_id'])
        else: 
            #No sabemos si el -1
            category_id = -1
        exist_category  = mp.contains(categories, category_id)

        if exist_category: 
            entry = mp.get(categories,category_id)
            category = me.getValue(entry)

        else: 
            category = newCategory(category_id)
            mp.put(categories,category_id,category)

        lt.addlast(category['videos'],video)

    except Exception:
        return None
        


# Funciones para creacion de datos
def newCategory(category_id):
    """
    Crea una nueva estructura para modelar los videos de un category id
    """
    category_dict = {'id': 0, "videos": None}
    category_dict['id'] = category_id
    category_dict['videos'] = lt.newList(datastructure='ARRAY_LIST')
    return category_dict


def newCountry(country):
    """
    Crea una nueva estructura para modelar los videos de un pais
    """
    country_dict = {'name': '', "videos": None}
    country_dict['name'] = country
    country_dict["videos"] = lt.newList(datastructure='ARRAY_LIST')
    return country_dict


def newCategoryId(id, name):
    """
    Crea un diccionario en el que guarda el nombre de la categoria y su id correpondiente
    """
    category = {'id': '', 'name': ''}
    category['id'] = int(id)
    category['name'] = name.strip()
    return category

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideoIdsLt(id1, id2):
    if id1['video_id'] < id2['video_id']:
        return -1
    elif id1['video_id'] > id2['video_id']:
        return 1
    else:
        return 0

def cmpVideoIds(id, entry):
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

def cmpVideoCategories(id, entry):
    catentry = me.getKey(entry)
    if (int(id) == int(catentry)):
        return 0
    elif (int(id) > int(catentry)):
        return 1
    else:
        return -1
# Funciones de ordenamiento

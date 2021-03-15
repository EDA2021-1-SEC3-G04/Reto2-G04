"""
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
               'category-id': None}

    catalog['videos'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['by_countries'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpCountries)
    catalog['by_categories'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpCategories)
    catalog['category-id'] = lt.newList(datastructure='ARRAY_LIST')
    return catalog


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    """
    Se añade un video a a lista de videos
    """
    lt.addLast(catalog['videos'], video)
    country = video['country'].strip()
    category = int(video['category_id'].strip())

    # Funciones para añadir datos a las listas de pais y categoria
    addVideoCountry(catalog, country, video)
    addVideoCategory(catalog, category, video)


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

def addVideoCategory(catalog, category_id, video):
    """
    Adiciona una categoria a lista de categorias si este no esta.
    Las listas de cada pais guarda referencias a los videos de dicho pais
    """
    categories_list = catalog['by_categories']
    posCategory = lt.isPresent(categories_list, category_id)

    if posCategory > 0:  # La categoria ya ha sido creada dentro de la lista
        category = lt.getElement(categories_list, posCategory)
    else:  # Debemos crear una nueva categoria
        category = newCategory(category_id)
        lt.addLast(categories_list, category)

    lt.addLast(category['videos'], video)


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

# Funciones de ordenamiento

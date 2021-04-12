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
from DISClib.Algorithms.Sorting import mergesort as mer
assert cf

"""
Se define la estructura de un catálogo de videos.
"""


# Construccion de modelos
def newCatalog():
    """
    Se define la estructura de un catálogo de videos. El catálogo tendrá tres 4, una para los videos, una para los category ids, otra para las categorias de los mismos y otra para los paises de los mismos.
    """
    catalog = {'videos': None,
               'by_countries': None,
               'by_categories': None,
               'category-id': None}

    catalog['videos'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpVideoIdsLt)

    # TODO: este es el que toca cambiar el maptype y el loadfactor!
    catalog['by_categories'] = mp.newMap(97, 
                                        maptype='PROBING', 
                                        loadfactor=0.5, 
                                        comparefunction=cmpVideoCategoriesId)

    catalog['category-id'] = mp.newMap(97, 
                                        maptype='PROBING', 
                                        loadfactor=0.5,   
                                        comparefunction=cmpVideoCategories)

    catalog['by_countries'] = mp.newMap(19, 
                                        maptype='PROBING', 
                                        loadfactor=0.5,
                                        comparefunction=cmpVideoCountries)
    return catalog

# Funciones para agregar informacion al catalogo
def addVideo(catalog, video):
    """
    Se añade un video a a lista de videos
    """
    lt.addLast(catalog['videos'], video)

    # Funciones para añadir datos a las listas de pais y categoria
    addVideoCountry(catalog, video)
    addVideoCategory(catalog, video)


def addCategory(catalog, category):
    """
    Se añade una categoria (su id y nombre) a a lista de categoria
    """
    id = int(category['id'])
    name = category['name'].strip()
    mp.put(catalog['category-id'], name, id)


def addVideoCountry(catalog, video):
    """
    Adiciona un pais a lista de paises.
    Las listas de cada pais guarda referencias a los videos de dicho pais
    """
    try: 
        countries = catalog['by_countries']
        if video['country'] != '': 
            country_name = (video['country'])
        else: 
            # No sabemos si el -1
            country_name = " "
        exist_country = mp.contains(countries, country_name)

        if exist_country: 
            entry = mp.get(countries, country_name)
            country_list = me.getValue(entry)

        else: 
            country_list = newCountry(country_name)
            mp.put(countries, country_name, country_list)

        lt.addLast(country_list['videos'],video)

    except Exception:
        return None


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
            # No sabemos si el -1
            category_id = -1
        exist_category = mp.contains(categories, category_id)

        if exist_category:
            entry = mp.get(categories, category_id)
            category = me.getValue(entry)

        else:
            category = newCategory(category_id)
            mp.put(categories, category_id, category)

        lt.addLast(category['videos'], video)

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





# Funciones de consulta
def getCategoryId(catalog, category):
    """
    Busca y retorna el ID asociado a una categoria, si no existe retorna None
    """
    exists_category = mp.contains(catalog['category-id'], category)
    category_id = None
    if exists_category: 
        category_id_pair = mp.get(catalog['category-id'], category)
        category_id = me.getValue(category_id_pair)
    return category_id


def getCategory(catalog, category_id):
    category_list = mp.get(catalog['by_categories'], category_id)
    category_list = me.getValue(category_list)
    return category_list


def getCountry(catalog, country): 
    country = mp.get(catalog['by_countries'], country)
    if country is not None: 
        country = me.getValue(country)
    return country


def videoSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['videos'])


def categorySize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['category-id'])


# REQUERIMEIENTO 1
def findTopsCountryCategory(sorted_cat_list, number, country): 
    """
    Requerimiento 1
    Crea una lista con los x videos con más views que corresponda a un  pais de una lista ordenada por views. 
    """
    topVideos = lt.newList(datastructure='ARRAY_LIST')
    pos = 1
    while number > 0 and pos < lt.size(sorted_cat_list): 
        video = lt.getElement(sorted_cat_list, pos)
        if video['country'] == country: 
            lt.addLast(topVideos, video)
            number -= 1
        pos += 1

    return topVideos

# REQUERIMIENTO 2
def findTopVideoCountries(country_list):
    """
    Requerimiento 2
    Crea lista con una estructura para modelar cada video y las veces que este aparece dentro de una lista (cuantos dias ha sido trending). 
    Con esa lista determina cuale de los videos ha tenido más dias trending. 
    """
    pos = 1
    reps_per_video = lt.newList(datastructure='ARRAY_LIST')
    current_reps = 1
    while pos < lt.size(country_list) - 1:
        current_elem = lt.getElement(country_list, pos)
        next_elem = lt.getElement(country_list, pos + 1)

        if current_elem['video_id'] != '#NAME?' and current_elem['video_id'] == next_elem['video_id']:
            current_reps += 1
        else:
            video_data = mp.newMap(5, maptype='PROBING', loadfactor=0.5)
            mp.put(video_data, 'video', current_elem)
            mp.put(video_data, 'reps', current_reps)
            current_reps = 1
            lt.addLast(reps_per_video, video_data)

        pos += 1

    top_video = ""
    top_reps = 0
    for item in lt.iterator(reps_per_video):
        reps = me.getValue(mp.get(item, 'reps'))
        if reps > top_reps:
            top_reps = reps
            top_video = me.getValue(mp.get(item, 'video'))

    return top_video, top_reps


# REQUERIMIENTO 3
def findTopVideo(category_list):
    """
    Requerimiento 3
    Crea lista con una estructura para modelar cada video y las veces que este aparece dentro de una lista (cuantos dias ha sido trending). 
    Con esa lista determina cuale de los videos ha tenido más dias trending. 
    """
    pos = 1
    reps_per_video = lt.newList(datastructure='ARRAY_LIST')
    current_reps = 1
    while pos < lt.size(category_list) - 1:
        current_elem = lt.getElement(category_list, pos)
        next_elem = lt.getElement(category_list, pos + 1)

        if current_elem['video_id'] != '#NAME?' and current_elem['video_id'] == next_elem['video_id']:
            current_reps += 1
        else:
            video_data = mp.newMap(5, maptype='PROBING', loadfactor=0.5)
            mp.put(video_data, 'video', current_elem)
            mp.put(video_data, 'reps', current_reps)
            current_reps = 1
            lt.addLast(reps_per_video, video_data)

        pos += 1

    top_video = ""
    top_reps = 0
    for item in lt.iterator(reps_per_video):
        reps = me.getValue(mp.get(item, 'reps'))
        if reps > top_reps:
            top_reps = reps
            top_video = me.getValue(mp.get(item, 'video'))

    return top_video, top_reps


# REQUERIMIENTO 4
def findWithTags(catalog, country, tag):
    country_pair = mp.get(catalog["by_countries"], country)
    country_list = me.getValue(country_pair)
    tag_list = lt.newList(datastructure='ARRAY_LIST')
    for video in lt.iterator(country_list["videos"]):
        current_tags = video['tags']
        if tag in current_tags:
            lt.addLast(tag_list, video)
    return tag_list


def findMostLikes(list_by_likes, number):
    """
    Requerimiento 4
    Crea una lista con los x videos con más likes dentro de una lista que ya esta ordenada. 
    Si un video ya se encuntra en la lista no lo repite. 
    """
    pos = lt.size(list_by_likes)
    topVideos = lt.newList(datastructure='ARRAY_LIST', cmpfunction=cmpVideoIdsLt)
    if pos > 0:
        lt.addLast(topVideos, lt.lastElement(list_by_likes))
        number -= 1
        while number > 0 and pos > 0:
            current_element = lt.getElement(list_by_likes, pos)
            pos_present = lt.isPresent(topVideos, current_element)
            if pos_present == 0:
                lt.addLast(topVideos, current_element)
                number -= 1
            pos -= 1     
    return topVideos


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
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1


def cmpVideoCategoriesId(id, entry):
    catentry = me.getKey(entry)
    if (int(id) == int(catentry)):
        return 0
    elif (int(id) > int(catentry)):
        return 1
    else:
        return -1


def cmpVideoCategories(id, entry):
    catentry = me.getKey(entry)
    if (id == catentry):
        return 0
    elif (id > catentry):
        return 1
    else:
        return -1


def cmpVideoCountries(country, count_entry):
    ctentry = me.getKey(count_entry)
    if (country) == (ctentry):
        return 0
    elif (country) > (ctentry):
        return 1
    else:
        return -1


def cmpLikes(video1, video2): 
    return int(video1['likes']) < int(video2['likes'])


def compVideosByViews(video1, video2):
    views1 = int(video1["views"])
    views2 = int(video2["views"])

    if views1 == views2:
        return 0
    elif views1 > views2:
        return 1
    else:
        return 0


def cmpVideoIdSort(video1, video2):
    return video1['video_id'] < video2['video_id']


# Funciones de ordenamiento
def sortLikes(video_list): 
    likes_sort = video_list.copy()
    likes_sort = mer.sort(likes_sort, cmpLikes)
    return likes_sort


def sortViews(catalog):
    sub_list = catalog.copy()
    sorted_list = mer.sort(sub_list, compVideosByViews)
    return sorted_list


def sortVideoId(category_list):
    vid_id_sort = category_list.copy()
    vid_id_sort = mer.sort(vid_id_sort, cmpVideoIdSort)
    return vid_id_sort


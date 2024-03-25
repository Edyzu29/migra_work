import time

from data import *
from sender_stand_request import *
import json
import pandas as pd
import rpy2.robjects as robjects
import sys
from datetime import datetime
from Constantes import *
###################################################
def open_json():
    print("Abrir data")
    with open("./data.json", "r") as data:
        data_json = json.load(data)
    print("DATA EXTRAIDA")
    return data_json
###################################################
def generador_json():
    json_pet = {key:dict() for key in nom_tablas}

    json_pet[nom_tablas[0]] = {key:0 for key in camp_cabecera}

    cantidad_campos = iter(camp_tablas)

    for index_tablas in range(1, len(nom_tablas)):
        
        limite = next(cantidad_campos)
            
        for campo in range(limite, limite + 15):
            
                json_pet[nom_tablas[index_tablas]]["fd" + str(campo)] = ""
                
    return json_pet
####################################################
def eliminar_datos(json_data):

    for nom_tab in nom_tablas:
                   
        llaves = list(json_data[nom_tab].keys())
        
        for key in llaves:
            
            if json_data[nom_tab][key] == "" or json_data[nom_tab][key] == 'nan':
                json_data[nom_tab].pop(key)
                
    return json_data
#####################################################
def reubicar_data(data, json_req, linea):

    campos_old_db = data[linea].keys()
    for campo_old in campos_old_db:

        valor_camp = data[linea][campo_old]

        if campo_old in old2new.keys():

            tabla_new, campo_new = old2new[campo_old]

            if campo_old == "FECHA_DATA_LOGER":

                dia = datetime.strptime(valor_camp, "%m/%d/%Y")
                valor_camp = dia.strftime("%d/%m/%y")

            if campo_old == "PBAR":

                #datos altiguos estan en mmhg
                #pasar a Hectopascales
                valor_camp = valor_camp*CONSTANTE_MMHG_2_HECTO

            json_req[tabla_new][campo_new] = valor_camp


    return json_req
######################################################
def agregar_tocken_identi(json_data):

    tabla_tocken = nom_tablas[0]
    campo_tocken = "token"
    campo_codigo = "id_estacion"
    campo_nome = "nombre_estacion"

    tabla_adicional = nom_tablas[-1]
    campo_migra = "fd207"

    # codigo_estacion = json_data[tabla_tocken][campo_codigo]
    codigo_estacion = 16 #ELIMINAR
    json_data[tabla_tocken][camp_cabecera[0]] = codigo_estacion #ELIMINAR

    nom_estacion = id_estaciones[codigo_estacion]
    json_data[tabla_tocken][campo_nome] = nom_estacion
    json_data[tabla_tocken][campo_tocken] = TOKEN[codigo_estacion]
    json_data[tabla_adicional][campo_migra] = IDENTIFICADOR_MIGRACION

    return  json_data
######################################################
def crear_archivo(ruta):
    request_ruta = "request_json/" + ruta + ".txt"
    with open(request_ruta, 'w') as archivo:
        pass
def guarda_request(json_data, ruta):
    request_ruta = "request_json/" + ruta + ".txt"
    with open(request_ruta, 'a') as archivo:
        json.dump(json_data, archivo, indent=4)
##########################################
def animacion_carga(actual, extra, carga):
    caracteres_animacion = ['|', '/', '-', '\\']
    nivel_carga = actual % len(caracteres_animacion)

    porcentaje = actual * 100.0 / carga

    sys.stdout.write('\rCargando ' + caracteres_animacion[nivel_carga] + extra + f' {porcentaje}% ')
    sys.stdout.flush()
############################################
def enviar_data ():
    pass
from proceso import *

ruta_1 = "Correcto"
ruta_2 = "Errores"
reporte_alertar = list()

if __name__ == '__main__':

    crear_archivo(ruta_1)
    crear_archivo(ruta_2)

    data = open_json()

    # totalidad_lineas = len(data)
    totalidad_lineas = 16
    for i in range(0, totalidad_lineas):
        json_request = generador_json()
        json_request = reubicar_data(data, json_request, i)
        json_request = agregar_tocken_identi(json_request)
        json_request = eliminar_datos(json_request)
        respuesta = post_data(json_request)
        animacion_carga(i, f' Codigo http: {respuesta.status_code}', totalidad_lineas)

        if respuesta.status_code != 200:
            ruta = ruta_2
        else:
            ruta = ruta_1

        guarda_request(json_request, ruta)

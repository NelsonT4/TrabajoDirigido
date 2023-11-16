import json
import base64
import requests

from applications.productos.ScrapyPages.DataCharge import saveProductsAndPrices
from .jumboCategory import obtener_categorias
from urllib.parse import urlencode

def cargarProductosJumbo():

    headers = {
            # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
            #"Origin": "https://domicilios.tiendasd1.com",
            "Referer": "",
            "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }

    variables = {
               "hideUnavailableItems":True,
               "skusFilter":"ALL_AVAILABLE",
               "simulationBehavior":"default",
               "installmentCriteria":"MAX_WITHOUT_INTEREST",
               "productOriginVtex":False,
               "map":"",
               "query":"",
               "orderBy":"OrderByTopSaleDESC",
               "from":0,
               "to":0,
               "selectedFacets":"",
               "facetsBehavior":"Static",
               "categoryTreeBehavior":"default",
               "withFacets":False,
               "variant":""
        }
    constante = {
            "workspace": "master",
            "maxAge": "short",
            "appsEtag": "remove",
            "domain": "store",
            "locale": "es-CO",
            "__bindingId": "2aad81c0-c729-41f4-a13b-002deae8039a",
            "operationName": "productSearchV3",
            "variables": {},
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "40b843ca1f7934d20d05d334916220a0c2cae3833d9f17bcb79cdd2185adceac",
                    "sender": "vtex.store-resources@0.x",
                    "provider": "vtex.search-graphql@0.x"
                },
                "variables": ""
            }
        }
    url_parameters = {
            "workspace": constante["workspace"],
            "maxAge": constante["maxAge"],
            "appsEtag": constante["appsEtag"],
            "domain": constante["domain"],
            "locale": constante["locale"],
            "__bindingId": constante["__bindingId"],
            "operationName": constante["operationName"],
            "variables": constante["variables"],
            "extensions": ""
        }

    categorias = obtener_categorias()
    Total_Productos = []
    for categoria in categorias:
        url_referecia =  "https://www.tiendasjumbo.co" + categoria["slug"]
        maps = ""
        query = categoria["slug"][1:]
        value_keys = query.split("/")
        session = requests.Session()
        selectedFacets = []
        for value_key in value_keys:
            maps += "," + "c"
            selectedFacets.append({
                "key": "c",
                "value": value_key
            })
        maps = maps[1:]

        headers["Referer"] = url_referecia

        #session = requests.Session()
        variables["map"] =maps
        variables["query"]=query
        variables["selectedFacets"]=selectedFacets

        num_productos = 100
        tam_bloque = 20
        inicio = 0

        while inicio < num_productos:

            fin = min(inicio + tam_bloque, num_productos)

            variables["from"]=inicio
            variables["to"]=fin

            #Delete Space del json
            variables_json = json.dumps(variables).replace(" ", "")
            #print(variables_json)
            variables_base64 = base64.b64encode(variables_json.encode('utf-8')).decode('utf-8')

            constante["extensions"]["variables"]=variables_base64

            url_parameters["extensions"] = constante["extensions"]


            url_api = "https://www.tiendasjumbo.co/_v/segment/graphql/v1?" + urlencode(url_parameters).replace("+", "")
            url_api = url_api.replace("%27", "%22")
            #print(url_api)
            try :
                response = session.get(url_api, headers=headers)
                data = response.json()

                productos = data.get("data", {}).get("productSearch", {}).get("products", [])
                num_productos = data.get("data", {}).get("productSearch", {}).get("recordsFiltered")
            except:
                print("error de consulta")
            inicio = fin + 1



            for producto in productos:
                Precio = producto.get("items", [{}])[0].get("sellers", [{}])[0].get("commertialOffer", {})
                Total_Productos.append({
                    "id": producto.get("productId"),
                    "almacen":"Jumbo",
                    "categoria": producto.get("categories")[0],
                    "marca": producto.get("brand"),
                    "nombre": producto.get("productName"),
                    "precio": Precio.get("spotPrice"),
                    "descripcion": producto.get("description").replace("\n*", "").replace("\n", ""),
                    "precioUnitario": Precio.get("Price"),#Precio Unitario
                })


    saveProductsAndPrices(Total_Productos)


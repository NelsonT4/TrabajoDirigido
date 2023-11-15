import base64
import json
import requests

from applications.productos.ScrapyPages.DataCharge import saveProductsAndPrices


class Pagina:

    def __init__(self,producto_buscar):

        self.producto_buscar = producto_buscar
        self.listaDeProductosFiltrada = []

        self.referencia = "https://www.exito.com/"+producto_buscar+"?_q="+producto_buscar+"&map=ft"

        self.headers = {
            "Referer": self.referencia,
            "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Content-type": "application/json"
        }

        self.url_base = "https://www.exito.com/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=es-CO&__bindingId=2f829b4f-604f-499c-9ffb-2c5590f076db&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2240b843ca1f7934d20d05d334916220a0c2cae3833d9f17bcb79cdd2185adceac%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22"

        self.url_variable = {
            "hideUnavailableItems": True,
            "skusFilter": "ALL_AVAILABLE",
            "simulationBehavior": "default",
            "installmentCriteria": "MAX_WITHOUT_INTEREST",
            "productOriginVtex": False,
            "map": "ft", "query": producto_buscar,
            "orderBy": "OrderByScoreDESC",
            "from": 0,
            "to": 1,
            "selectedFacets": [
                {"key": "ft", "value": producto_buscar}],
            "fullText": producto_buscar,
            "facetsBehavior": "dynamic",
            "categoryTreeBehavior": "default",
            "withFacets": False,
            "variant": "T6gNSyhuONOUSPhbmY8zZ:651c1b8ef1ae3a1e6ebc80da-variantNull"
        }

        # Se le quitan espacios a la parte variable de la url
        url_variable_string = json.dumps(self.url_variable).replace(" ", "")

        # Se codifica en base64 la parte variable
        url_variable_base64 = base64.b64encode(url_variable_string.encode('utf-8')).decode('utf-8')

        # Se une la parte constante y variable codificada en base64
        self.url_api = self.url_base + url_variable_base64 + "%22%7D"

        self.getJson()

    def getJson(self):
        self.response = requests.get(self.url_api, headers=self.headers)
        self.json = self.response.json()

        return self.json

    #Obtiene la lista de productos del almacen
    def getProductosPorPagina(self):

        listaProductosPagina = []
        listaDeProductosSinFiltrar = self.json["data"]["productSearch"]["products"]

        for producto in listaDeProductosSinFiltrar:
            listaProductosPagina.append(self.getDatosProducto(producto))

        return listaProductosPagina

    #crea un archivo json con el contenido de la pagina en la ruta actual
    def crearJson(self,nombreJson):
        with open(nombreJson, "w") as f:
            json.dump(self.json, f)

    def modificarLimitesApi(self,inicio,fin):
        self.url_variable = {
            "hideUnavailableItems": True,
            "skusFilter": "ALL_AVAILABLE",
            "simulationBehavior": "default",
            "installmentCriteria": "MAX_WITHOUT_INTEREST",
            "productOriginVtex": False,
            "map": "ft", "query": self.producto_buscar,
            "orderBy": "OrderByScoreDESC",
            "from": inicio,
            "to": fin,
            "selectedFacets": [
                {"key": "ft", "value": self.producto_buscar}],
            "fullText": self.producto_buscar,
            "facetsBehavior": "dynamic",
            "categoryTreeBehavior": "default",
            "withFacets": False,
            "variant": "T6gNSyhuONOUSPhbmY8zZ:651c1b8ef1ae3a1e6ebc80da-variantNull"
        }

        # Se le quitan espacios a la parte variable de la url
        url_variable_string = json.dumps(self.url_variable).replace(" ", "")

        # Se codifica en base64 la parte variable
        url_variable_base64 = base64.b64encode(url_variable_string.encode('utf-8')).decode('utf-8')

        # Se une la parte constante y variable codificada en base64
        self.url_api = self.url_base + url_variable_base64 + "%22%7D"

    def getProductos(self):
        self.cantProductos = self.json["data"]["productSearch"]["recordsFiltered"]

        productosObtenidos = 0
        while ((self.cantProductos - productosObtenidos) >= 100):
            self.modificarLimitesApi(0+productosObtenidos,99+productosObtenidos)
            self.getJson()
            self.listaDeProductosFiltrada.extend(self.getProductosPorPagina())
            productosObtenidos += 100

        self.modificarLimitesApi(productosObtenidos,self.cantProductos-1)
        self.getJson()
        self.listaDeProductosFiltrada.extend(self.getProductosPorPagina())

        return self.listaDeProductosFiltrada

    def getDatosProducto(self,diccionario_producto):

        producto = {"id": diccionario_producto["productId"],
                    "almacen": "Exito",
                    "categoria": diccionario_producto["categories"][0],
                    "marca": diccionario_producto["brand"],
                    "descripcion": diccionario_producto["productName"],
                    "precio": diccionario_producto["priceRange"]["sellingPrice"]["lowPrice"]
                    }

        return producto

def cargarProductosExito(productos_a_buscar):

    for producto_a_buscar in productos_a_buscar:
        page_exito_for_product = Pagina(producto_a_buscar)
        lista_de_productos = page_exito_for_product.getProductos()

        saveProductsAndPrices(lista_de_productos)













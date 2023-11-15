from applications.productos.ScrapyPages.productosExito import Pagina
from DataCharge import saveProductsAndPrices

producto_a_buscar = "Televisores"

page_exito_for_product = Pagina(producto_a_buscar)
lista_de_productos = page_exito_for_product.getProductos()

saveProductsAndPrices(lista_de_productos)
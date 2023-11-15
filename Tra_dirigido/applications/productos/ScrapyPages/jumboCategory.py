import requests
def obtener_categorias():
    headers = {
        # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
        "Referer": "https://www.tiendasjumbo.co/",
        "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Content-type": "application/json"
    }

    session = requests.Session()

    query = """
        query getMenu @context(sender: "tiendasjumboqaio.jumbo-main-menu@2.0.3") {
            menus @runtimeMeta(hash: "70d5fd9e572a3503ba9eb7659e347426e403f8cfeddc4bb56f40834985c1cbfe"){
                id
                name    
                slug    
                icon    
                display   
                menu {     
                    id     
                    name     
                    slug      
                    menu {        
                        id       
                        name       
                        slug    
                        __typename    
                    }      
                    __typename
                }    
                __typename  
            }
        }
    """

    json_data = {
        "query": query,
        #"variables": variables
    }


    url_api = 'https://www.tiendasjumbo.co/_v/private/graphql/v1?workspace=master&maxAge=long&appsEtag=remove&domain=store&locale=es-CO'
    response = session.post(url_api, headers=headers, json=json_data)
    data = response.json()
    #print(data)
    categorias = data.get("data", {}).get("menus", [{}])

    Lista_Categorias = []

    for categoria in categorias:
        categoriaPadre= categoria.get("menu", [{}])
        for categoriaHijo in categoriaPadre:
            Lista_Categorias.append({
                "nameFather": categoria.get("name"),
                "slugFather": categoria.get("slug"),
                "name": categoriaHijo.get("name"),
                "slug": categoriaHijo.get("slug")
            })
    return Lista_Categorias

if __name__ == "__main__":
    resultado = obtener_categorias()
    print(resultado)
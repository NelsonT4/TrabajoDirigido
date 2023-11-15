import requests
from urllib.parse import quote
def obtener_categorias():
    headers = {
        "Referer": "https://domicilios.tiendasd1.com",
        "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "content-type": "application/json"
        #"X-Goog-Api-Key": "AIzaSyDIx3k5l142QNUDito5bsxVdRsSj2LA8gk"
    }

    session = requests.Session()

    query = """
      fragment CategoryFields on CategoryModel {
      active
      boost
      hasChildren
      categoryNamesPath
      isAvailableInHome
      level
      name
      path
      reference
      slug
      photoUrl
      imageUrl
      shortName
      isFeatured
      isAssociatedToCatalog
      __typename
    }
    
    fragment CategoriesRecursive on CategoryModel {
      subCategories {
        ...CategoryFields
        subCategories {
          ...CategoryFields
          subCategories {
            ...CategoryFields
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    
    fragment CategoryModel on CategoryModel {
      ...CategoryFields
      ...CategoriesRecursive
      __typename
    }
    
    query GetCategoryTree($getCategoryInput: GetCategoryInput!) {
      getCategory(getCategoryInput: $getCategoryInput) {
        ...CategoryModel
        __typename
      }
    }
    """

    getCategoryInput= {
        "clientId": "D1",
        "storeReference": "11808"
    }
    variables = {
        "getCategoryInput": getCategoryInput
    }

    json_data = {
        'query': query,
        "variables": variables
    }
    url_api = 'https://nextgentheadless.instaleap.io/api/v3'
    response = session.post(url_api, headers=headers, json=json_data)

    data = response.json()
    categorias = data.get("data", []).get("getCategory", {})

    Lista_Categorias  = []

    for categoria in categorias:
        direccion = categoria.get("slug")
        categoryReference = direccion.split("/")
        categoryReference = quote(categoryReference[1], safe='').replace("25" ,"")

        #print(categoryReference)
        Lista_Categorias.append({
            "name": categoria.get("name"),
            "slug": categoria.get("slug"),
            "categoryReference": categoryReference
        })
    return Lista_Categorias

if __name__ == "__main__":
    resultado = obtener_categorias()
    print(resultado)

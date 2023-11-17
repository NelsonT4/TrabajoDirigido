from .DunoCategory import obtener_categorias
import requests
import json
from .DataCharge import saveProductsAndPrices

def cargarProductosD1():

    categorias = obtener_categorias()
    #print(categorias)
    headers = {
        "Origin": "https://domicilios.tiendasd1.com",
        "Referer": "",
        "User-Agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "content-type": "application/json"
        }
    query = """
          query GetProductsByCategory(
            $getProductsByCategoryInput: GetProductsByCategoryInput!
          ) {
            getProductsByCategory(
              getProductsByCategoryInput: $getProductsByCategoryInput
            ) {
              category {
                ...CategoryWithProductsModel
              }
              pagination {
                ...PaginationModel
              }
              aggregates {
                ...AggregateModel
              }
              banners {
                ...BannerModel
              }
              promoted {
                ...PromotedModel
              }
            }
          }
        fragment CategoryWithProductsModel on CategoryWithProductsModel {
            name
            reference
            level
            path
            hasChildren
            active
            boost
            isAvailableInHome
            slug
            photoUrl
            categoryNamesPath
            imageUrl
            shortName
            isFeatured
            products {
              ...CatalogProductModel
            }
          }
          fragment PaginationModel on PaginationModel {
            page
            pages
            total {
              ...PaginationTotalModel
            }
          }
          fragment AggregateModel on AggregateModel {
            name
            docCount
            buckets {
              ...AggregateBucketModel
            }
          }
          fragment BannerModel on BannerModel {
            id
            storeId
            title
            desktopImage
            mobileImage
            targetUrl
            targetUrlInfo {
              type
              url
            }
            targetCategory
            index
            categoryId
          }
          fragment PromotedModel on PromotedModel {
            isPromoted
            onLoadBeacon
            onClickBeacon
            onViewBeacon
            onBasketChangeBeacon
            onWishlistBeacon
          }
          fragment AggregateBucketModel on AggregateBucketModel {
            min
            max
            key
            docCount
          }
          fragment PaginationTotalModel on PaginationTotalModel {
            value
            relation
          }
          fragment CatalogProductModel on CatalogProductModel {
            name
            price
            photosUrl
            unit
            subUnit
            subQty
            description
            sku
            ean
            maxQty
            minQty
            clickMultiplier
            nutritionalDetails
            isActive
            slug
            brand
            stock
            securityStock
            boost
            isAvailable
            location
            promotion {
              ...Promotion
            }
            categories {
              ...CategoryFields
            }
            categoriesData {
              ...CategoryFields
            }
            formats {
              ...CatalogProductFormatModel
            }
            tags {
              ...CatalogProductTagModel
            }
            specifications {
              ...SpecificationModel
            }
            promoted {
              ...PromotedModel
            }
            score
            relatedProducts
            ingredients
            stockWarning
          }
          fragment Promotion on Promotion {
            type
            isActive
            conditions {
              ...PromotionCondition
            }
            description
            endDateTime
            startDateTime
          }
    
          fragment PromotionCondition on PromotionCondition {
            quantity
            price
          }
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
          }
          fragment CatalogProductFormatModel on CatalogProductFormatModel {
            format
            equivalence
            unitEquivalence
          }
          fragment CatalogProductTagModel on CatalogProductTagModel {
            description
            enabled
            textColor
            filter
            tagReference
            backgroundColor
            name
          }
          fragment SpecificationModel on SpecificationModel {
            title
            values {
              label
              value
            }
          }
        """
    getProductsByCategoryInput = {
        "categoryReference": "",
        "categoryId": "null",
        "clientId": "D1",
        "storeReference": "11808",
        "currentPage": 1,
        "pageSize": 1000,
        "filters": {},
        # "sort": {},
        "googleAnalyticsSessionId": ""
    }

    Total_Productos = []
    for categoria in categorias:
        url_referencia = "https://domicilios.tiendasd1.com/ca/" + categoria["slug"]

        headers["Referer"] = url_referencia
        session = requests.Session()
        getProductsByCategoryInput["categoryReference"] = categoria["categoryReference"]

        variables = {
            "getProductsByCategoryInput": getProductsByCategoryInput
        }

        json_data = {
            'query': query,
            "variables": variables
        }

        #url_api = 'https://firebase.googleapis.com/v1alpha/projects/-/apps/1:609017978746:web:0b92eac5636d59905f80c3/webConfig'
        #response = session.get(url_api, headers=headers)
        #print(response)

        url_api = 'https://nextgentheadless.instaleap.io/api/v3'
        response = session.post(url_api, headers=headers, json=json_data)

        data = response.json()
        productos = data.get("data", {}).get("getProductsByCategory", {}).get("category", {}).get("products",[])
        #print(productos)

        for producto in productos:
            categoria = producto.get("categories", [{}])[0]
            #print(categoria)
            Total_Productos.append({
                "id": producto.get("sku"),
                "almacen": "D1",
                "categoria": categoria.get("name"),
                "marca": producto.get("brand"),
                "nombre": producto.get("name"),
                "precio": producto.get("price"),
                "descripcion": producto.get("description").replace("<br />", " "),



                "precioUnitario": round(producto.get("price")/producto.get("subQty"), 2),
            })
        #print(Total_Productos)

    saveProductsAndPrices(Total_Productos)


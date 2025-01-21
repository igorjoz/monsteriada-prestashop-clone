import json
import random
import prestapyt
 
URL = "http://localhost:8080/api/"
API_KEY = "F2WY4KDW76DP99L7H7RDLJGUZQJBFHYW"
        
def remove_empty_fields_from_product(product):
    product = product['product']
    keys_to_remove = []
    for key in product:
        if product[key] == '':
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del product[key]
    return {'product': product}
 
def add_images(path, product_id):
    path = f"./web-scraper/scraped-data/img/img-large{path}"
    file_name = path.split('/')[-1]
    try:
        fd = open(path, 'rb')
        img = fd.read()
        fd.close()
    
        ps.add('/images/products/' + str(product_id), files=[('image', f"{file_name}.jpg", img)])
    except FileNotFoundError as e:
        print(f"Failed to add image: {path}. Error: {e}")
 
def modify_stock(product_id, availability):
    if availability == "Dostępny":
        quantity = 10
    else: quantity = 0
    
    stock = ps.get('stock_availables', options={'filter[id_product]': product_id, 'display': 'full'})
    stock['stock_availables']['stock_available']['quantity'] = quantity
    ps.edit(f'stock_availables/{product_id}', {'stock_available': stock['stock_availables']['stock_available']})
        
def check_if_product_should_belong(path, title):
    with open (path) as f:
        data = json.load(f)
        for product in data['categoryContent']:
            if product['title'] == title:
                return True
    return False
 
def process_temp_categories(product_to_be_added):
    temp_categories = []
    
    # promocje
    if check_if_product_should_belong("./web-scraper/scraped-data/promocje.json", product_to_be_added['title']):
        temp_categories.append(ps.get('categories', options={'filter[name]': 'Promocje'})['categories']['category']['attrs']['id'])
        
    # nowosci
    if check_if_product_should_belong("./web-scraper/scraped-data/nowosci.json", product_to_be_added['title']):
        temp_categories.append(ps.get('categories', options={'filter[name]': 'Nowości'})['categories']['category']['attrs']['id'])
        
    # bestsellery
    if check_if_product_should_belong("./web-scraper/scraped-data/bestsellery.json", product_to_be_added['title']):
        temp_categories.append(ps.get('categories', options={'filter[name]': 'Bestsellery'})['categories']['category']['attrs']['id'])
        
    return temp_categories
    
def existing_product(product_to_be_added, category_id): # also check if product should belong in nowosci, promocje or/and bestsellery
    print(f"Product already exists: {product_to_be_added['title']}")
    product = ps.get('products', options={'filter[name]': product_to_be_added['title'], 'display': 'full'})
    if 'products' not in product or 'product' not in product['products']:
        print("Error: 'products' or 'product' key not found in product")
        return
 
    product_data = product['products']['product']
    if 'associations' in product_data and 'categories' in product_data['associations']:
        product_categories = product_data['associations']['categories']['category']
        product_categories.append({'id': category_id})
        # product already exists scenario ocurrs only when the data from second file is being imported, so theres empty "WSZYSTKIE PRODUKTY" category that has to be filled with every product
        # WARNING this might NOT WORK properly in case the first scraped file wasnt fully imported
        try:
            product_categories.append({'id': ps.get('categories', options={'filter[name]': 'WSZYSTKIE PRODUKTY'})['categories']['category']['attrs']['id']})
            temp_categories = process_temp_categories(product_to_be_added) # bestsellery, nowosci, promocje check
            for temp_category in temp_categories:
                product_categories.append({'id': temp_category})
        except TypeError as e:
            print(f"Failed to get category id for 'WSZYSTKIE PRODUKTY'. Error: {e}")
        
        if 'manufacturer_name' in product_data:
            del product_data['manufacturer_name']
        if 'quantity' in product_data:
            del product_data['quantity']
        if 'categories' in product_data:
            del product_data['categories']
        product_data['associations']['categories']['category'] = product_categories
        ps.edit(f'products/{product_data["id"]}', {'product': product_data})
        print(f"Product {product_to_be_added['title']} categories updated")
    else:
        print("Error: 'associations' or 'categories' key not found in product")
        
def fill_with_basic_product_data(product, product_to_be_added, category_id):
    product['product']['name']['language']['value'] = product_to_be_added['title']
    product['product']['description']['language']['value'] = product_to_be_added['moreData'][0]['productDescriptionContent']
    product['product']['description_short']['language']['value'] = product_to_be_added['shortDescription']
    product['product']['price'] = str(product_to_be_added['priceData']['price'])
    product['product']['active'] = 1
    product['product']['id_category_default'] = int(category_id)
    product['product']['associations']['categories'] = {
        "category": [
            {'id': category_id},
            {'id': 1},
        ]
    }
    product['product']['id_manufacturer'] = 0
    product['product']['id_supplier'] = 0
    product['product']['id_shop_default'] = 1
    product['product']['state'] = 1
    product['product']['on_sale'] = 0
    product['product']['active'] = 1
    product['product']['available_for_order'] = 1
    product['product']['show_price'] = 1
    product['product']['tags'] = {
        "tag": [
            {'id': str(product_to_be_added['available'])},
        ]
    }
    
    return product
 
def remove_all_features():
    features = ps.get('product_features')
    if not features['product_features']:
        print("No features to remove")
        return
    
    for f in features['product_features']['product_feature']:
        feature_id = f['attrs']['id']
        try:
            ps.delete('product_features', resource_ids=feature_id)
            print(f"Deleted feature with id: {feature_id}")
        except prestapyt.prestapyt.PrestaShopWebServiceError as e:
            print(f"Failed to delete feature with id: {feature_id}. Error: {e}")
    
def add_features(product, product_to_be_added):
    details = product_to_be_added['moreData'][1]['productDetailsContent']
    features = {}
    combined_features = []
    
    # get the features from scraped data
    for detail in details.split("<dt class=\"name\">")[1:]:
        name, rest = detail.split("</dt>", 1)
        value = rest.split("<dd class=\"value\">")[1].split("</dd>")[0]
        value = value.replace('<br>', '').replace('\n', ' ').strip()
        features[name.strip()] = value.strip()
        
    # check if the feature and feature value already exist in db
    for feature_name, feature_value in features.items():
        if ps.get('product_features', options={'filter[name]': feature_name})['product_features'] == '':
            feature = ps.get('product_features', options={'schema': 'blank'})
            feature['product_feature']['name']['language']['value'] = feature_name
            try:
                ps.add('product_features', feature)
            except prestapyt.prestapyt.PrestaShopWebServiceError as e:
                print(f"Failed to add new feature: {feature_name}. Error: {e}")
        
        if ps.get('product_feature_values', options={'filter[value]': feature_value})['product_feature_values'] == '':    
            feature_id = ps.get('product_features', options={'filter[name]': feature_name})['product_features']['product_feature']['attrs']['id']
            value = ps.get('product_feature_values', options={'schema': 'blank'})
            value['product_feature_value']['value']['language']['value'] = feature_value
            value['product_feature_value']['id_feature'] = feature_id
            try:
                ps.add('product_feature_values', value)
            except prestapyt.prestapyt.PrestaShopWebServiceError as e:
                print(f"Failed to add new feature value: {feature_value}. Error: {e}")
                
        # add the features to the product        
        feature_id = ps.get('product_features', options={'filter[name]': feature_name})['product_features']['product_feature']['attrs']['id']
        feature_value_id = ps.get('product_feature_values', options={'filter[value]': feature_value})['product_feature_values']['product_feature_value']['attrs']['id']
        product_feature = {
            "id": feature_id,
            "id_feature_value": feature_value_id
        }
        
        if product_feature not in combined_features:
            combined_features.append(product_feature)
        
    product['product']['associations']['product_features']['product_feature'] = combined_features
    return product
    
def add_product(product_to_be_added, category_id):
    if 'title' not in product_to_be_added:
        print("Error: 'title' key not found in product_to_be_added")
        return
 
    response = ps.get('products', options={'filter[name]': product_to_be_added['title']})
    if 'products' not in response:
        print("Error: 'products' key not found in response")
        return
    
    # check if the product already exists in db to avoid duplicates
    if response['products']:
        existing_product(product_to_be_added, category_id)
        return
 
    product = ps.get('products', options={'schema': 'blank'})
    
    # fill the product with basic data
    product = fill_with_basic_product_data(product, product_to_be_added, category_id)
    
    # add features
    product = add_features(product, product_to_be_added)
    
    # remove empty fields from product
    product = remove_empty_fields_from_product(product)
 
    # add the product to db
    try:
        product_id = ps.add('products', product)
        modify_stock(product_id['prestashop']['product']['id'], product_to_be_added['available'])
        for img_path in product_to_be_added['locationsOfImgLargeResources']:
            add_images(img_path, product_id['prestashop']['product']['id'])
        print(f"Added product: {product_to_be_added['title']}")
    except prestapyt.prestapyt.PrestaShopWebServiceError as e:
        print(f"Failed to add product: {product_to_be_added['title']}. Error: {e}")
    
 
def add_single_category(name, parent_id=2):
    category = ps.get('categories', options={'schema': 'blank'})
    category['category']['name']['language']['value'] = name
    category['category']['link_rewrite']['language']['value'] = name.lower().replace(" ", "-")
    category['category']['active'] = 1
    category['category']['id_parent'] = parent_id
    
    try:
        saved_category = ps.add('categories', category)
        print(f"Added category: {name}")
        return int(saved_category['prestashop']['category']['id'])
    except prestapyt.prestapyt.PrestaShopWebServiceError as e:
        print(f"Failed to add category: {name}. Error: {e}")
        return None
        
def add_scraped_data(file_path):
    # read json file
    with open(file_path) as f:
        data = json.load(f)
        categories = data['categoryName'] # root category
        # add root category
        main_category_id = add_single_category(categories, 2)
        
        if main_category_id is None:
            print(f"Failed to add main category: {categories}")
            return
        
        # add subcategories and sub-subcategories
        categories = data['categoryContent']
        
        for category in categories:
            category_name = category['subcategoryName']
            category_id = add_single_category(category_name, main_category_id)
            
            if category_id is None:
                continue
            else:
                try:
                    for subcategory in category['subCategoryContent']:
                        subcategory_name = subcategory['sub-subcategoryName']
                        subcategory_id = add_single_category(subcategory_name, category_id)
                        # add products that belong to sub-sub categories
                        for product in subcategory['sub-subcategoryContent']:
                            add_product(product, subcategory_id)
                            
                except KeyError:
                    print(f"No subcategories for category: {category_name}")
                    subcategory_name = category_name
                    subcategory_id = category_id
                    # add products that belong to sub categories
                    for product in category['subCategoryContent']:
                        add_product(product, subcategory_id)
        
def get_all_categories():
    print("All currently available categories:")
    #print(ps.get('categories', options={'display': "full"})) # debug
    print(ps.get('categories',))
        
def get_all_products():
    print("All currently available products:")
    #print(ps.get('products', options={'display': "full"})) # debug
    print(ps.get('products'))
 
def remove_all_products():
    products = ps.get('products')
    if not products['products']:
        print("No products to remove")
        return
    
    for p in products['products']['product']:
        product_id = p['attrs']['id']
        try:
            ps.delete('products', resource_ids=product_id)
            print(f"Deleted product with id: {product_id}")
        except prestapyt.prestapyt.PrestaShopWebServiceError as e:
            print(f"Failed to delete product with id: {product_id}. Error: {e}")
    print("All products removed")
    
def remove_existing_categories():
    categories = ps.get('categories')
    if 'categories' not in categories or not categories['categories']['category']:
        print("No categories to remove")
        return
    
    for c in categories['categories']['category']:
        category_id = int(c['attrs']['id'])
        if category_id in [1, 2]:
            continue
        try:
            ps.delete('categories', resource_ids=category_id)
            print(f"Deleted category with id: {category_id}")
        except prestapyt.prestapyt.PrestaShopWebServiceError as e:
            print(f"Failed to delete category with id: {category_id}. Error: {e}")
    print("All categories removed")
    
    
def update_tax_and_stock(): # changing tax to 23% (theres no tax information in scraped data) and setting stock to 10 if product is available (task requirements)
    products = ps.get('products')
    if not products['products']:
        print("No products to update")
        return
    else:
        for p in products['products']['product']:
            # tax
            product_id = p['attrs']['id']
            product = ps.get('products', options={'filter[id]': product_id, 'display': 'full'})
            product = product['products']['product']
            price = float(product['price']) / 1.23
            product['id_tax_rules_group'] = '1'
            
            # need to update the price after changing the tax group
            product['price'] = f"{price:.2f}"
            
            # remove these fields from product to avoid errors, but keep the stock info
            if 'manufacturer_name' in product:
                del product['manufacturer_name']
            
            if 'quantity' in product:
                del product['quantity']
                
            ps.edit(f'products/{product_id}', {'product': product})
            print(f"Product {product['name']['language']['value']} tax updated")
            
            # stock
            try:
                response = ps.get('stock_availables', options={'filter[id_product]': product_id, 'display': 'full'})
                quantity = response['stock_availables']['stock_available']['quantity']
                if not quantity == '0':
                    modify_stock(product_id, "Dostępny")
                    print(f"Product {product['name']['language']['value']} stock updated")
            except prestapyt.prestapyt.PrestaShopWebServiceError as e:
                print(f"Failed to update stock for product: {product['name']['language']['value']}. Error: {e}")
                continue
            except KeyError as e:
                print(f"KeyError: {e} in response for product {product_id}: {response}")
                continue
            except TypeError as e:
                print(f"TypeError: {e} in response for product {product_id}: {response}")
                continue
            
        print("All products updated")
        
if __name__ == "__main__":
    ps = prestapyt.PrestaShopWebServiceDict(URL, API_KEY)
    
    # remove all the feautures
    # remove_all_features()
    
    # remove all products
    # remove_all_products()
    # get_all_products()
    
    # remove all categories
    # remove_existing_categories()
    # get_all_categories()
    
    # add_single_category("Nowości", 2)
    # add_single_category("Promocje", 2)
    # add_single_category("Bestsellery", 2)
    
    # add scrapped products and categories to db
    # print("Gadzety wg kategorii")
    # add_scraped_data("./web-scraper/scraped-data/gadzetyWgKategorii.json")
    # print("Gadzety wg tematyki")
    # add_scraped_data("./web-scraper/scraped-data/gadzetyWgTematyki.json")
    
    # update tax and stock
    update_tax_and_stock()
    
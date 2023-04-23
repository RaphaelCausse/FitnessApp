from django.core.cache import cache
from .models import Account, Food, Meal, Result
import openfoodfacts as off
import datetime as dt

def get_calories_of_the_day(request):
    context = {}
    account = Account.objects.get(user=request.user)
    try:
        result = Result.objects.get(owner=account, date=dt.date.today())
    except Result.DoesNotExist:
        result = Result.objects.create(owner=account, date=dt.date.today())
        result.save()
    
    goalCalories = account.goalCalories
    caloriesConsumed = 0
    for mealType in Meal.MealType:
        try:
            meal = Meal.objects.get(mealType=mealType, result=result)
            foods = Food.objects.filter(meal=meal)
            caloriesConsumed += sum([food.energy for food in foods])
            context[mealType.name.lower()] = round(sum([food.energy for food in foods]) / goalCalories * 100, 2)
        except:
            context[mealType.name.lower()] = 0
    
    context["calories_to_consume"] = round((goalCalories - caloriesConsumed) / goalCalories * 100, 2)
    return context

def autocomplete_products(pattern):
    products = [
        {
            "name": item['name'],
            "energy": item['energy'],
            "lipid": item['lipid'],
            "carbohydrate": item['carbohydrate'],
            "protein": item["protein"],
        } for item in Food.objects.filter(name__contains=pattern, meal__isnull=True).values()
    ]
    indexes_products = [product['name'].find(pattern) for product in products]
    products = [product for _, product in sorted(zip(indexes_products, products), key=lambda x: x[1]['name'])]
    return products

def create_product_obj(off_products, start_index, n):
    products = []
    if off_products is None:
        return None

    for i in range(start_index, n if n < len(off_products) else len(off_products)):
        product_data = {
            "name": off_products[i].get("product_name") or
                next(off_products[i][key] for key in off_products[i].keys()
                    if "product_name" in key),

            "img": off_products[i].get("image_front_url", "")
        }
        if product_data["name"] == "":
            continue

        nutrients = {
            "energy": "energy-kcal", "lipid": "fat", "carbohydrate": "carbohydrates",
            "sugar": "sugars", "protein": "proteins", "fiber": "fiber", "water": "water"
        }
        for key, value in nutrients.items():
            try:
                product_data[key] = round(float(off_products[i]["nutriments"][f"{value}_100g"]), 2)
            except KeyError:
                product_data[key] = 0

        products.append(product_data)

    return products

def search_product(product, product_index):
    products = cache.get(product)
    if products is None:
        cache.clear()
        off_products = off.products.search(product, page_size = 10)['products']
        products = create_product_obj(off_products, 0, 10)
        cache.set(product, products)
    elif (product_index >= len(products)):
        off_products = off.products.search(product, page_size = product_index + 5)['products']
        products += create_product_obj(off_products, product_index, product_index + 5)
        cache.set(product, products)
    
    return products[product_index] if product_index < len(products) else None


def add_product_to_db(product):
    food = Food(
        name=product['name'],
        energy=product['energy'],
        lipid=product['lipid'],
        carbohydrate=product['carbohydrate'],
        sugar=product['sugar'],
        protein=product['protein'],
        fiber=product['fiber'],
        water=product['water'],
        label=Food.FoodLabel.INGR
    )
    food.save()
    return food

def add_product_to_user(user, data):
    account = Account.objects.get(user=user)
    result = Result.objects.get(date=dt.date.today(), owner=account)
    
    food = Food.objects.get(name=data['name'], meal__isnull=True)

    nutrients = {key: int(getattr(food, key)) * (int(data["quantity"]) / 100) for key in ["energy", "lipid", "carbohydrate", "sugar", "protein", "fiber", "water"]}

    

    mealPeriod = {
        "petit-dejeuner": Meal.MealType.BREAKFAST,
        "collation": Meal.MealType.MORNING_SNACK,
        "dejeuner": Meal.MealType.LUNCH,
        "gouter": Meal.MealType.SNACK,
        "diner": Meal.MealType.DINNER
    }.get(data["period"])

    try:
        meal = Meal.objects.get(result=result, mealType=mealPeriod)
    except Meal.DoesNotExist:
        meal = Meal.objects.create(result=result, mealType=mealPeriod)
        meal.save()
    
    updateFood = Food.objects.create(
        meal=meal,
        name=food.name,
        energy=nutrients['energy'],
        lipid=nutrients['lipid'],
        carbohydrate=nutrients['carbohydrate'],
        sugar=nutrients['sugar'],
        protein=nutrients['protein'],
        fiber=nutrients['fiber'],
        water=nutrients['water'],
        label=food.label
    )

    updateFood.save()
     
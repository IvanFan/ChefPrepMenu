import random
from breakfast_dishes import breakfast_dishes
from lunch_main_dishes import lunch_main_dishes
from lunch_side_dishes import lunch_side_dishes
from breafast_starchy_foods import breakfast_starchy_foods
from lunch_starchy_foods import lunch_starchy_foods
from scope import ALL_FAMILY, ONLY_MY_WIFE, ONLY_ME
from tabulate import tabulate



# As a new family, we would like to try different dishes every week. This script can automatically generate
# 5-days breakfast & lunch menu for us. We use it for food preparation.

# breakfast rule
# 1 starchy food for my wife and 1 starchy food for me
# 1 eggs per person

# lunch rule
# 1 main dish and 1 side dish every day.
# 1 starchy food every day e.g. brown rice, taco or noodles

def get_breakfast_starchy_food(is_my_wife=False, is_me=False):
    if is_my_wife:
        special_weight_for_my_wife = random.randrange(0, 10)
        if special_weight_for_my_wife >= 7:
            return {
                "name": "4in1",
                "description": "a special combination of oats, very healthy",
                "scope": ONLY_MY_WIFE
            }

    dishes = []
    for dish in breakfast_starchy_foods:
        if is_me:
            if "scope" not in dish or dish["scope"] == ONLY_ME:
                dishes.append(dish)
        else:
            if "scope" not in dish or dish["scope"] == ALL_FAMILY:
                dishes.append(dish)
    dish_index = random.randrange(0, len(dishes))
    return dishes[dish_index]


def get_dish(is_my_wife=False, dishes=[]):
    if is_my_wife:
        my_wife_dishes = []
        for dish in dishes:
            if "scope" in dish and dish["scope"] == ONLY_MY_WIFE:
                my_wife_dishes.append(dish)
        dish_index = random.randrange(0, len(my_wife_dishes))
        return my_wife_dishes[dish_index]
    else:
        my_dishes = []
        for dish in dishes:
            if "scope" in dish and dish["scope"] != ONLY_MY_WIFE:
                my_dishes.append(dish)
        dish_index = random.randrange(0, len(my_dishes))
        return my_dishes[dish_index]


def get_weekly_menu():
    daily_menus = []
    for i in range(5):
        daily_menus.append({
            "breakfast": {
                "starchy_food":{
                    "wife": None,
                    "me": None
                },
                "dishes": {
                    "wife": None,
                    "me": None
                }
            },
            "lunch": {
                "main": None,
                "side": None,
                "starchy_food": None
            }
        })

    for daily_menu in daily_menus:
        # breakfast
        daily_menu["breakfast"]["starchy_food"]["wife"] = get_breakfast_starchy_food(is_my_wife=True)
        if "scope" in daily_menu["breakfast"]["starchy_food"]["wife"] and\
                daily_menu["breakfast"]["starchy_food"]["wife"]["scope"] == ONLY_MY_WIFE:
            daily_menu["breakfast"]["starchy_food"]["me"] = get_breakfast_starchy_food(is_my_wife=False, is_me=True)
        else:
            daily_menu["breakfast"]["starchy_food"]["me"] = \
                daily_menu["breakfast"]["starchy_food"]["wife"]

        daily_menu["breakfast"]["dishes"]["wife"] = get_dish(is_my_wife=True, dishes=breakfast_dishes)
        daily_menu["breakfast"]["dishes"]["me"] = get_dish(is_my_wife=False, dishes=breakfast_dishes)

        # lunch
        daily_menu["lunch"]["main"] = get_dish(is_my_wife=False, dishes=lunch_main_dishes)
        daily_menu["lunch"]["side"] = get_dish(is_my_wife=False, dishes=lunch_side_dishes)
        daily_menu["lunch"]["starchy_food"] = get_dish(is_my_wife=False, dishes=lunch_starchy_foods)
    return daily_menus


weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]
weekly_menu = get_weekly_menu()
print("#############################")
print("Breakfast & Lunch Weekly Menu")
print("#############################")
for i in range(len(weekly_menu)):
    curr_menu = weekly_menu[i]
    print("############# {} Menu #############".format(weekdays[i]))
    print(tabulate(
        [
            ['Wife', curr_menu["breakfast"]["starchy_food"]["wife"]["name"], curr_menu["breakfast"]["dishes"]["wife"]["name"], '', curr_menu["lunch"]["main"]["name"], curr_menu["lunch"]["side"]["name"], curr_menu["lunch"]["starchy_food"]["name"]],
            ['Me', curr_menu["breakfast"]["starchy_food"]["me"]["name"], curr_menu["breakfast"]["dishes"]["me"]["name"], '','','','']
        ],
        headers=['Breakfast', 'Starchy Food', 'Dish', 'Lunch', 'Main', 'Side', 'Starchy Food'],
        tablefmt='orgtbl'))
print("############# End #############")





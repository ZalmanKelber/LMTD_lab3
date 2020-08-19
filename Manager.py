from Ingredients import Ingredient_list, Recipe
import urllib.request
import urllib.parse
import json
import ssl

class Query:
    def __init__(self):
        self.apiKey = "7b5b37c8578948dcac885363273e39e6"
        self.fillIngredients = True
        self.includeIngredients = ""
        self.query = ""

    def set_ingredients(self, ingredients: list):
        self.includeIngredients = ",".join(ingredients)

    def set_query(self, term: str):
        self.query = term


class Manager:
    def __init__(self):
        self.pantry = Ingredient_list("pantry")
        self.recipes = list()
        self.needed = Ingredient_list("needed ingredients")
        self.shopping = Ingredient_list("shopping list")

    def __dict__(self):
        print("calling __dict__ in manager class")
        result = {
        "pantry": self.pantry.__dict__(),
        "recipes": list(map(lambda r: r.__dict__(), self.recipes)),
        "needed": self.needed.__dict__(),
        "shopping": self.shopping.__dict__()
        }
        return result

    def __str__(self):
        result = self.pantry.__str__()
        for r in self.recipes:
            result += "\n" + r.__str__()
        result += "\n" + self.needed.__str__()
        result += "\n" + self.shopping.__str__()
        return result

    def view_pantry(self):
        print(self)
        print(self.pantry)

    def change_pantry(self):
        choice = input("do you wish to add or remove items from the pantry? (0 to exit)\n")
        if choice == 0:
            return
        if choice.lower() not in "add" and choice.lower() not in "remove":
            print("couldn't read answer\n")
            return
        add = choice.lower() in "add"
        item = input("which ingredient do you wish to {0}?\n".format("add" if add else "remove"))
        if add:
            self.pantry.add_ingredient(item)
        else:
            self.pantry.remove_ingredient(item)

    def view_recipes(self):
        if len(self.recipes) == 0:
            print("no recipes in recipe list\n")
            return
        for recipe in self.recipes:
            print(recipe)

    def change_recipes(self):
        choice = input("do you wish to add or remove recipes from the recipe list? (0 to exit)\n")
        if choice == 0:
            return
        if choice.lower() not in "add" and choice.lower() not in "remove":
            print("couldn't read answer")
            return
        if choice.lower() in "add":
            self.add_recipes()
        else:
            self.remove_recipes()

    def remove_recipes(self):
        for recipe in self.recipes:
            print("   " + recipe.name)
        to_remove = input("which of the above recipes do you wish to remove?\n")
        found = False
        for recipe in self.recipes:
            if to_remove.lower().strip() in recipe.name.lower().strip():
                found = True
                self.recipes.remove(recipe)
                print("removed {0} from recipe list\n".format(to_remove))
        if not found:
            print("didn't locate {0}\n".format(to_remove))
            return
        self.needed = Ingredient_list("needed ingredients")
        for recipe in self.recipes:
            self.add_to_needed(recipe)

    def add_recipes(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        q = Query()
        q.set_ingredients(self.pantry.ingredients)
        term = input("What would you like to search for? (0 to exit)\n")
        if term == 0:
            return
        q.set_query(term)
        search_url = "https://api.spoonacular.com/recipes/complexSearch?" + urllib.parse.urlencode(q.__dict__)
        print(search_url)
        req = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx) as response:
            json_response = json.loads(response.read().decode("utf-8"))
            for recipe in json_response["results"]:
                print(recipe["title"])
            loop = True
            while loop:
                choice = input("Which recipe do you wish to add? (0 to exit)\n")
                if choice == 0:
                    return
                for recipe in json_response["results"]:
                    if choice.lower().strip() in recipe["title"].lower().strip():
                        ingredients = list()
                        for ingredient in recipe["usedIngredients"]:
                            ingredients.append(ingredient["name"])
                        for ingredient in recipe["missedIngredients"]:
                            ingredients.append(ingredient["name"])
                        r = Recipe(recipe["title"], ingredients)
                        self.recipes.append(r)
                        self.add_to_needed(r)
                        print("successfully added {0} to recipes".format(recipe["title"]))
                cont = input("do you wish to add another recipe? (y/n)\n")
                if cont.lower()[0] != "y":
                    loop = False

    def add_to_needed(self, recipe):
        for ingredient in recipe.ingredients:
            if ingredient not in self.pantry.ingredients and ingredient not in self.needed.ingredients:
                self.needed.add_ingredient(ingredient, print_result=False)


    def view_needed(self):
        print(self.needed)

    def view_shopping(self):
        print(self.shopping)

    def change_shopping(self):
        choice = input("do you wish to add or remove items from the shopping list? (0 to exit) ")
        if choice == 0:
            return
        if choice.lower() not in "add" and choice.lower() not in "remove":
            print("couldn't read answer")
            return
        add = choice.lower() in "add"
        item = input("which ingredient do you wish to {0}?\n".format("add" if add else "remove"))
        if add:
            self.shopping.add_ingredient(item, from_stock=True, stock=self.needed)
        else:
            self.shoppinh.remove_ingredient(item)

    @classmethod
    def from_json(cls, data: dict):
        m = Manager()
        for ingredient in data["pantry"]["ingredients"].keys():
            m.pantry.add_ingredient(ingredient, print_result=False)
        m.recipes = list(map(lambda r: Recipe(r["name"], r["ingredients"]),data["recipes"]))
        for ingredient in data["needed"]["ingredients"].keys():
            m.needed.add_ingredient(ingredient, print_result=False)
        for ingredient in data["shopping"]["ingredients"].keys():
            m.shopping.add_ingredient(ingredient, print_result=False)
        return m

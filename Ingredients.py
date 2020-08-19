class Ingredient_list:
    def __init__(self, name: str):
        self.name = name
        self.ingredients = dict()

    def __dict__(self):
        return {"name": self.name, "ingredients": self.ingredients}

    def __str__(self):
        return "{0}: {1} ingredient(s)\n".format(self.name, len(self.ingredients.keys()))

    def add_ingredient(self, ingredient: str, print_result=True, from_stock=False, stock=None):
        if from_stock and ingredient not in stock.ingredients:
            proceed = input("{0} is not listed in {1}.  Would you like to add it to {2} anyway?  (y/n)\n".format(ingredient, stock.name, self.name))
            if proceed.lower() not in "yes":
                return
        self.ingredients[ingredient] = True
        if print_result:
            print("successfully added {0} to {1}\n".format(ingredient, self.name))

    def remove_ingredient(self, ingredient: str, print_result=True):
        if ingredient not in self.ingredients:
            print("ingredient not found\n")
            return
        del self.ingredients[ingredient]
        if print_result:
            print("successfully removed {0} from {1}\n".format(ingredient, self.name))

    def __str__(self):
        if not bool(self.ingredients):
            return "{0} is currently empty\n".format(self.name)
        result = "items in {0}:\n".format(self.name)
        for ingredient in self.ingredients:
            result += "     {0}\n".format(ingredient)
        return result

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)

class Recipe:
    def __init__(self, name: str, ingredients: list):
        self.name = name
        self.ingredients = ingredients

    def __dict__(self):
        return {"name": self.name, "ingredients": self.ingredients}

    def __str__(self):
        result = "recipe: " + self.name + "\n"
        for ingredient in self.ingredients:
            result += "    " + ingredient + "\n"
        return result

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)

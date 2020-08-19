import sys
from Manager import Manager
import json

class Menu:
    #user interface to interact that guides interaction with portfolio
    def __init__(self, m=Manager()):
        self.manager = m
        self.choices = [
        {"name": "exit", "action": self.exit},
        {"name": "view current pantry", "action": self.manager.view_pantry},
        {"name": "add or remove items from pantry", "action": self.manager.change_pantry},
        {"name": "view current recipes", "action": self.manager.view_recipes},
        {"name": "search and add or remove recipes", "action": self.manager.change_recipes},
        {"name": "view needed ingredients", "action": self.manager.view_needed},
        {"name": "view shopping list", "action": self.manager.view_shopping},
        {"name": "add or remove items from shopping list", "action": self.manager.change_shopping},
        {"name": "save or retrieve data", "action": self.save_or_retrieve}
        ]

    def display_greeting(self):
        print("\n\n*********************")
        print("Welcome to Pantry, your personal ingredient and recipe manager!")

    def display_menu(self):
        print("\nHow would you like to proceed?\n\n")
        for i in range(len(self.choices)):
            print("to {0}, enter {1}\n".format(self.choices[i]["name"], i))

    def run(self):
        self.display_greeting()
        while True:
            self.display_menu()
            choice = input("Enter selection: ")
            print("\n")
            try:
                action = self.choices[int(choice)]["action"]
            except:
                print("Invalid selection.  Please enter a number between 0 and {0}".format(len(self.choices)))
                break
            action()

    def save_or_retrieve(self):
        choice = input("do you wish to save or retrieve data? (s/r, 0 to exit)\n")
        if choice == 0:
            return
        if choice.lower()[0] != "s" and choice.lower()[0] != "r":
            print("couldn't recognize response")
            return
        if choice.lower()[0] == "s":
            with open("manager.json", "w") as outfile:
                data = json.dumps(self.manager.__dict__())
                outfile.write(data)
                print("saved data")
        else:
            with open("manager.json", "r") as f:
                data = json.loads(f.read())

                m = Manager.from_json(data)
                Menu(m).run()

    def exit(self):
        print("Thank you for visiting Pantry")
        sys.exit(0)

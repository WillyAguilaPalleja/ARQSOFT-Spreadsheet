from entities.spreadsheet import UserInterface

if __name__ == '__main__':
    UI1 = UserInterface()
    UI2 = UserInterface()
    print(UI1.controller is UI2.controller)

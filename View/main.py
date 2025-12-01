from Controller.ControllerProbManager import ControllerProbManager
from View.MainView import MainView

if __name__ == "__main__":
    controller = ControllerProbManager()
    app = MainView(controller)
    app.mainloop()

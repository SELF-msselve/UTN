from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class MiWidget(GridLayout):
    pass

class MiApp(App):
    def build(self):
        return MiWidget()

if __name__ == '__main__':
    MiApp().run() 
from kivy.app import App
from kivy.uix.stacklayout import StackLayout

class MiWidget(StackLayout):
    pass

class MiApp(App):
    def build(self):
        return MiWidget()

if __name__ == '__main__':
    MiApp().run()
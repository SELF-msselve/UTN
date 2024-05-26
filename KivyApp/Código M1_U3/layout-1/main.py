from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget

class MiWidget(Widget):
    pass

class MiApp(App):
    def build(self):
        return MiWidget()

if __name__ == '__main__':
    MiApp().run()

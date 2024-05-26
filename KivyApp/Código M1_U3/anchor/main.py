from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class MiWidget(FloatLayout):
    pass

class MiApp(App):
    def build(self):
        return MiWidget()

if __name__ == '__main__':
    MiApp().run()

    

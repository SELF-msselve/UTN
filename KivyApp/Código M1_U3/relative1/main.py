from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

class MiWidget(RelativeLayout):
    pass

class MiApp(App):
    def build(self):
        return MiWidget()

if __name__ == '__main__':
    MiApp().run()

    

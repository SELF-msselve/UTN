from kivy.app import App
from kivy.uix.pagelayout import PageLayout

class MiWidget(PageLayout):
    pass

class MiApp(App):
    def build(self):
        return MiWidget()

if __name__ == '__main__':
    MiApp().run()
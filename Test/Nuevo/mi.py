from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

class MainWindow(BoxLayout):
    def __init__(self, switch_callback, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Ventana Principal'))
        self.add_widget(Button(text='Ir a la segunda ventana', on_press=switch_callback))

class SecondWindow(BoxLayout):
    def __init__(self, switch_callback, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Segunda Ventana'))
        self.add_widget(Button(text='Volver a la ventana principal', on_press=switch_callback))

class MyApp(App):
    def build(self):
        self.root = BoxLayout()
        self.main_window = MainWindow(switch_callback=self.switch_to_second)
        self.second_window = SecondWindow(switch_callback=self.switch_to_main)
        self.root.add_widget(self.main_window)
        return self.root

    def switch_to_main(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.main_window)

    def switch_to_second(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.second_window)

if __name__ == '__main__':
    MyApp().run()

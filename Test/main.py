from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
#from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import pandas as pd
from pipe import Pipe

#df is your dataframe
#example function is applicable for all INT dataframe 

from random import randint
from kivy.properties import NumericProperty

class UnificaScreen():
    pipes = []
    GRAVITY = 300
    was_colliding = False
    pipe_diviation = 100
    
    dataOrden = [1,2,3,4,5,6,7,8,9,10]
    dataNombre = ['Lucas','Stella','Eduardo','Anto','Joyi', 'Yayo','Lucy','Alberto', 'Martin', 'XXXXX']
    dataScore = [1,2,3,4,5,6,7,8,9,10]
    data = {'Orden': dataOrden, 'Nombre': dataNombre, 'Score': dataScore}
    df_score = pd.DataFrame(data)

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create textures
        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)
        
    

    def on_size(self, *args):
        self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)
        self.floor_texture.uvsize = (self.width / self.floor_texture.width, -1)

    def scroll_textures(self, time_passed):
        # Update the uvpos of the texture
        self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + time_passed/2.0)%Window.width , self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ( (self.floor_texture.uvpos[0] + time_passed)%Window.width, self.floor_texture.uvpos[1])

        # Redraw the texture
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)


class Bird(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "bird1.png"
        super().on_touch_up(touch)




class ScoreWindow(BoxLayout, UnificaScreen):
    def __init__(self, **kwargs):
        super(ScoreWindow, self).__init__(**kwargs)
        start_button = Button(text="Start Game")
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)
        
    def start_game(self, instance):
        App.get_running_app().switch_to_GameWindow()
   

class GameWindow(FloatLayout, UnificaScreen):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
    
    pipes = []
    GRAVITY = 300
    was_colliding = False
    pipe_diviation = 100

    def pipe_deviation_easy(self):
        self.pipe_diviation = 200
        Pipe.GAP_SIZE = 200
        self.ids.lvl_1.disabled = True
        self.ids.lvl_2.disabled = False
        self.ids.lvl_3.disabled = False
        
    def pipe_deviation_med(self):
        self.pipe_diviation = 150
        Pipe.GAP_SIZE = 150
        self.ids.lvl_1.disabled = False
        self.ids.lvl_2.disabled = True
        self.ids.lvl_3.disabled = False
        
    def pipe_deviation_hard(self):
        self.pipe_diviation = 100
        Pipe.GAP_SIZE = 100
        self.ids.lvl_1.disabled = False
        self.ids.lvl_2.disabled = False
        self.ids.lvl_3.disabled = True

    #def on_start(self):
    #    Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)

    def move_bird(self, time_passed):
        bird = self.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        self.check_collision()

    def check_collision(self):
        bird = self.ids.bird
        # Go through each pipe and check if it collides
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(bird):
                is_colliding = True
                # Check if bird is between the gap
                if bird.y < (pipe.pipe_center - pipe.GAP_SIZE/2.0):
                    self.game_over()
                if bird.top > (pipe.pipe_center + pipe.GAP_SIZE/2.0):
                    self.game_over()
        if bird.y < 96:
            self.game_over()
        if bird.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.ids.score.text = str(int(self.ids.score.text)+1)
        self.was_colliding = is_colliding

  
    def game_over(self):
        # Crear una ventana emergente (popup)
        popup = Popup(title="Ventana Secundaria", size_hint=(0.8, 0.6))
        
        # Crear un layout para la ventana secundaria
        secondary_layout = BoxLayout(orientation="vertical")
        
        # Crear un campo de texto para ingresar texto
        text_input = TextInput(hint_text="Ingresa tu texto aquí")
        secondary_layout.add_widget(text_input)
        
        # Crear un botón para cerrar la ventana secundaria
        close_button = Button(text="Cerrar Ventana Secundaria")
        close_button.bind(on_press=popup.dismiss)
        secondary_layout.add_widget(close_button)
        
        # Agregar el layout a la ventana secundaria
        popup.content = secondary_layout
        
        # Mostrar la ventana secundaria
        popup.open()  
        
        self.clear_widgets()
        self.add_widget(ScoreWindow())
        
        
        self.ids.lvl_1.disabled = False
        self.ids.lvl_2.disabled = False
        self.ids.lvl_3.disabled = False
        self.ids.bird.pos = (20, (self.height - 96) / 2.0)
        for pipe in self.pipes:
            self.remove_widget(pipe)
        self.frames.cancel()
        self.ids.start_button.disabled = False
        self.ids.start_button.opacity = 1


    def next_frame(self, time_passed):
        self.move_bird(time_passed)
        self.move_pipes(time_passed)
        self.ids.background.scroll_textures(time_passed)

    def start_game(self):
        self.ids.lvl_1.disabled = True
        self.ids.lvl_2.disabled = True
        self.ids.lvl_3.disabled = True
        self.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        #Clock.schedule_interval(self.move_bird, 1/60.)
        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)

        # Create the pipes
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(96 + self.pipe_diviation, self.height - self.pipe_diviation)
            pipe.size_hint = (None, None)
            pipe.pos = (Window.width + i*distance_between_pipes, 96)
            pipe.size = (64, self.height - 96)

            self.pipes.append(pipe)
            self.add_widget(pipe)

        # Move the pipes
        #Clock.schedule_interval(self.move_pipes, 1/60.)

    def move_pipes(self, time_passed):
        # Move pipes
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        # Check if we need to reposition the pipe at the right side
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width
    

class MainApp(App):
    def build(self):
        #self.root = GameWindow()
        self = ScoreWindow()
        return self
    
    def switch_to_GameWindow(self):
        self.root.clear_widgets()
        self.root.add_widget(GameWindow())
    



if __name__ == "__main__":
    MainApp().run()

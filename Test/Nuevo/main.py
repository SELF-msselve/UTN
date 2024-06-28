from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from random import randint
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ObjectProperty, ListProperty

class MainApp(App):
    pipes = []
    GRAVITY = 300
    was_colliding = False
    pipe_diviation = 100
    def build(self):
        self.root = FloatLayout()
        self.main_window = ScoreWindow(switch_callback=self.switch_to_second)
        self.second_window = GameWindow(switch_callback=self.switch_to_main)
        self.root.add_widget(self.main_window)
        return self.root
    def switch_to_main(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.main_window)
    def switch_to_second(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.second_window)
class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + time_passed/2.0)%Window.width , self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ( (self.floor_texture.uvpos[0] + time_passed)%Window.width, self.floor_texture.uvpos[1])
        texture = self.property('cloud_texture')
        texture.dispatch(self)
        texture = self.property('floor_texture')
        texture.dispatch(self)
class Pipe(Widget):
    GAP_SIZE = NumericProperty(150)
    CAP_SIZE = NumericProperty(20)
    pipe_center = NumericProperty(0)
    bottom_body_position = NumericProperty(0)
    bottom_cap_position = NumericProperty(0)
    top_body_position = NumericProperty(0)
    top_cap_position = NumericProperty(0)
    pipe_body_texture = ObjectProperty(None)
    lower_pipe_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    top_pipe_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipe_body_texture = Image(source="pipe_body.png").texture
        self.pipe_body_texture.wrap = 'repeat'
    def on_size(self, *args):
        lower_body_size = self.bottom_cap_position - self.bottom_body_position
        self.lower_pipe_tex_coords[5] = lower_body_size/20.
        self.lower_pipe_tex_coords[7] = lower_body_size/20.
        top_body_size = self.top - self.top_body_position
        self.top_pipe_tex_coords[5] = top_body_size/20.
        self.top_pipe_tex_coords[7] = top_body_size/20.
    def on_pipe_center(self, *args):
        Clock.schedule_once(self.on_size, 0)
class Bird(Image):
    velocity = NumericProperty(0)
    def on_touch_down(self, touch):
        self.source = "bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)
    def on_touch_up(self, touch):
        self.source = "bird1.png"
        super().on_touch_up(touch)        
class GameWindow(FloatLayout, MainApp, Background, Bird, Pipe):
    def __init__(self, switch_callback, **kwargs):
        super().__init__(**kwargs)
    def start_game(self):
        # Window.ids.lvl_1.disabled = True
        # self.root.ids.lvl_2.disabled = True
        # self.root.ids.lvl_3.disabled = True
        # self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(96 + self.pipe_diviation, Window.height - self.pipe_diviation)
            pipe.size_hint = (None, None)
            pipe.pos = (Window.width + i*distance_between_pipes, 96)
            pipe.size = (64, Window.height - 96)
            self.pipes.append(pipe)
            Window.add_widget(pipe) #
    def next_frame(self, time_passed):
        self.move_bird(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_textures(time_passed)
    def move_bird(self, time_passed):
        bird = GameWindow.Bird.ids.bird #
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        self.check_collision()
    def pipe_deviation_easy(self):
        self.pipe_diviation = 200
        Pipe.GAP_SIZE = 200
        self.root.ids.lvl_1.disabled = True
        self.root.ids.lvl_2.disabled = False
        self.root.ids.lvl_3.disabled = False
    def pipe_deviation_med(self):
        self.pipe_diviation = 150
        Pipe.GAP_SIZE = 150
        self.root.ids.lvl_1.disabled = False
        self.root.ids.lvl_2.disabled = True
        self.root.ids.lvl_3.disabled = False
    def pipe_deviation_hard(self):
        self.pipe_diviation = 100
        Pipe.GAP_SIZE = 100
        self.root.ids.lvl_1.disabled = False
        self.root.ids.lvl_2.disabled = False
        self.root.ids.lvl_3.disabled = True
    def check_collision(self):
        bird = self.root.ids.bird
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(bird):
                is_colliding = True
                if bird.y < (pipe.pipe_center - pipe.GAP_SIZE/2.0):
                    self.game_over()
                if bird.top > (pipe.pipe_center + pipe.GAP_SIZE/2.0):
                    self.game_over()
        if bird.y < 96:
            self.game_over()
        if bird.top > Window.height:
            self.game_over()
        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.was_colliding = is_colliding
    def game_over(self):
        self.root.ids.lvl_1.disabled = False
        self.root.ids.lvl_2.disabled = False
        self.root.ids.lvl_3.disabled = False
        self.root.ids.bird.pos = (20, (self.root.height - 96) / 2.0)
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1
    def move_pipes(self, time_passed):
        for pipe in self.pipes:
            pipe.x -= time_passed * 100
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width
class ScoreWindow(FloatLayout, MainApp, Background, Bird, Pipe):
    def __init__(self, switch_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Ventana Principal'))
        self.add_widget(Button(text='Ir a la segunda ventana', on_press=switch_callback))
MainApp().run()

from logging import root
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.animation import Animation


class Gerenciador(ScreenManager):
    pass


class Player(Image):
    def on_touch_down(self, touch):
        if (touch.x >= 0) and (touch.x <= self.parent.width):
            self.center_x = touch.x
            print(f'Evento ')
            return True
        # return super(Player, self).on_touch_down(touch)


class Inimigo(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = Animation(y=-self.height, duration=7)
        # self.anim.bind(on_complete=self.vanish)
        self.anim.start(self)

    def vanish(self, *args):
        gameScreen = App.get_running_app().root.get_screen('GameOver')
        gameScreen.remove_widget(self)
        gameScreen.inimigos.remove(self)
        print("Objeto Removido")


class GameOver(Screen):
    class GameOver(Image):
        pass


class Tela(Screen):
    inimigos = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.desenharTela)
        # self.add_widget(Player())
        Clock.schedule_interval(self.putObstacle, 3)

    def putObstacle(self, *args):
        obstacle = Inimigo(y=self.width, height=400)
        self.add_widget(obstacle, 3)
        self.inimigos.append(obstacle)
        print("Objeto adcionado")

    def desenharTela(self, *args):
        self.add_widget(Player())
        # self.add_widget(Inimigo())

    def update(self, *args):
        if self.collided():
            self.gameOver()

    def gameOver(self, *args):
        Clock.unschedule(self.putObstacle, 1)
        for inimigo in self.inimigos:
            inimigo.anim.cancel(inimigo)
            self.remove_widget(ob)
        self.inimigos = []
        App.get_running_app().root.current = 'GameOver'

    def collided(self, wid1, wid2):
        if wid2.x <= wid1.x + wid1.height and \
                wid2.x + wid2.height > wid1.x and \
                wid2.y <= wid1.y + wid1.width and \
                wid2.y + wid2.width >= wid1.y:
            print("Colisao")
            return True
        return False

    def playerCollided(self):
        collided = False
        if self.collided((self.Player.pos, self.Player.size), (self.inimigos.pos, self.inimigos.size)):
            print("COLISAO DETECTADA")
            collided = True
        return collided


class Astronauta(App):
    pass


Astronauta().run()

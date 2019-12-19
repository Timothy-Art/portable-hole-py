from pyfiglet import Figlet


class Sketch(list):
    pass


class Layer:
    def __init__(self, x: int, y: int, sketch):
        self.pos = (x, y)
        self.sketch = sketch()

    def draw(self, canvas):
        for i, row in enumerate(self.sketch):
            for j, character in enumerate(row):
                if j:
                    canvas[i + self.pos[1], j + self.pos[0]] = character


class Element:
    def __init__(self, width: int, height: int):
        """
        Creates a new Element with size width by height.

        :param width: Width (x) of canvas
        :param height: Height (y) of canvas
        """
        self.width = width
        self.height = height
        self._state = [' ' * self.width for _ in range(self.height)]
        self._layers = []

    def __getitem__(self, item):
        x, y = item
        return self._state[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self._state[y][x] = value

    def draw(self, stdscr):
        pass

    def handle(self, stdscr):
        pass


class Title(Sketch):
    def __init__(self):
        fig = Figlet(font='larry3d')
        fig.width = 105
        title = fig.renderText('Portable Hole').split(sep='\n')[:-3]
        title.append(' ' * 4 + '_' * 94)
        title.append(' ' * 3 + '/\\' + '_' * 93 + '\\')
        title.append(' ' * 3 + '\\/' + '_' * 93 + '/')
        title.append(' ' * 4 + '-' * 70 + '\\Loot Management Systems\\')
        title.append(' ' * 75 + '-' * 24)

        super().__init__(*title)

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def intersect(self, other):
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1

    def center(self):
        x = (self.x1 + self.x2) // 2
        y = (self.y1 + self.y2) // 2
        return x, y

    def in_room(self, x, y):
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

    def on_border(self, x, y):
        return x == self.x1 or x == self.x2 or y == self.y1 or y == self.y2


# an automated bird! kind of like a bird and droid
class Boid:
    def __init__(self):
        self.position = PVector(random(width), random(height))
        self.velocity = PVector()
        self.acceleration = PVector()


    def show(self):
        strokeWeight(16)
        stroke(0, 0, 100)
        fill(0, 0, 100, 50)
        point(self.position.x, self.position.y)

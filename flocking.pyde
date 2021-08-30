# Kiwi, 2021.08.39
# Flocking Simulation with Daniel Shiffman at the Coding Train!
# This is coding challenge #124
# Flocking behavior follows:
#    separation: steer to avoid crowding local flockmates
#    alignment: steer toward the average heading of local flockmates
#    cohesion: steer to move toward the average position of local flockmates
#    object avoidance: ?
#

from boid import Boid
        
def setup():
    global flock
    
    size(640, 360)
    frameRate(40)
    colorMode(HSB, 360, 100, 100, 100)
    mono = createFont("terminus.ttf", 16);
    textFont(mono);   
    noSmooth()
    
    flock = []
    for i in range(80):
        flock.append(Boid())
        
    
def draw():    
    global flock
    
    background(209, 95, 33)
    fill(0, 0, 100)
    
    # display the entire flock
    for boid in flock:
        boid.edges()
        boid.flock(flock)
        boid.update()
        boid.show()
    
    fill(0, 0, 100)
    text("{:.0f}".format(frameRate), 20, 30)

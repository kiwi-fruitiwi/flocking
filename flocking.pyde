# Kiwi, 2021.08.39
# Flocking Simulation with Daniel Shiffman at the Coding Train!
# This is coding challenge #124
#
# 

from boid import Boid
        
def setup():
    global flock
    
    size(640, 360)
    frameRate(144)
    colorMode(HSB, 360, 100, 100, 100)
    mono = createFont("terminus.ttf", 16);
    textFont(mono);   
    noSmooth()
    
    flock = []
    for i in range(100):
        flock.append(Boid())
        
    
def draw():    
    global flock
    
    background(209, 95, 33)
    fill(0, 0, 100)
    
    # display the entire flock
    for boid in flock:
        boid.show()
    
    
    text("{:.0f}".format(frameRate), 20, 30)

# Kiwi, 2021.08.39
# Flocking Simulation with Daniel Shiffman at the Coding Train!
# This is coding challenge #124
# Flocking behavior follows:
# .  separation: steer to avoid crowding local flockmates
# .  alignment: steer toward the average heading of local flockmates
# .  cohesion: steer to move toward the average position of local flockmates
# .  9S hackbot show()
# .  quadtree
# .  seek, evade, mousepressed seek toggle, apply_force
#    reimplement seek and refactor alignment, cohesion, and separation with it
#    circle intersection
#    field of view arc in perception radius
#    object avoidance: ?
#    3D! uh oh, quaterion?
#    boids with different parameters. colored!
#    field of view rule! "flake"? keep the views clear

from boid import *
from quadtree import *
        
def setup():
    global boids, seek
    
    size(640, 360)
    rectMode(CORNER)
    colorMode(HSB, 360, 100, 100, 100)
    mono = createFont("terminus.ttf", 16);
    textFont(mono);
    
    boids = []
    seek = True # used as a toggle if we want the boids to seek a target
    for i in range(150):
        boids.append(Boid())
        
    
def draw():    
    global boids, seek
    
    background(209, 95, 33)
    fill(0, 0, 100)
    
    # generate a quadtree at the start of each frame
    # pass in the quadtree so we can query boids in the flock for their neighbors
    boundary = Rectangle(0, 0, width, height)
    qt = Quadtree(boundary, 4)
    
    for boid in boids:
        p = Point(boid.position.x, boid.position.y, boid)
        qt.insert(p)
    
    # display the entire flock
    # use our quadtree to query only boids within a certain radius
    # radius of bounding box
    R = 15
    for boid in boids:
        x = boid.position.x
        y = boid.position.y
        
        # we want a square boundary with our boid in the center 
        boundary = Rectangle(x-R, y-R, 2*R, 2*R)
        
        points = qt.query(boundary)
        boid_query_result = []
        for p in points:
            boid_query_result.append(p.data)        
        
        # print len(boid_query_result)
        # maybe flash display the boundary?
        
        # we used to send in the entire boids list but now we use our quadtree to
        # cut down comparison time
        # boid.flock(boids)
        
        
        boid.flock(boid_query_result)
        # steering = boid.seek_target(PVector(mouseX, mouseY))
        # if seek:
        #     boid.apply_force(steering)
        # else:
        #     boid.apply_force(steering.mult(-1)) # this replicates evade
    
        boid.show()

    qt.show()
    
    
    # update the flock
    for boid in boids:
        boid.update()
        boid.edges()
        
        
    # FPS counter display
    s = "FPS: {:.0f}".format(frameRate)
    pad = 5
    fill(0, 0, 100, 50)
    rect(12-pad, 24+pad, textWidth(s)+10, -22, 3) # weird that processing allows a negative h
    
    fill(0, 0, 100, 100)
    text(s, 12, 24)


def mousePressed():
    global seek
     
    seek = not seek

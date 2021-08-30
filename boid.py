
# an automated bird! kind of like a bird and droid
class Boid:
    def __init__(self):
        self.position = PVector(random(width), random(height))
        self.velocity = PVector().random2D().setMag(random(0.5, 1.5))
        self.acceleration = PVector()
        self.max_force = 0.2
        self.max_speed = 2


    # update the boid's position, velocity, and acceleration
    def update(self):
        self.position.add(self.velocity)
        self.velocity.add(self.acceleration)
        self.acceleration = PVector(0, 0)
                        

    def show(self):
        strokeWeight(8)
        stroke(0, 0, 100)
        fill(0, 0, 100, 50)
        point(self.position.x, self.position.y)
        
    
    # steer with limited perception of nearby neighbors
    
    # steer to avoid crowding local flockmates
    def separation(self):
        pass
        
    
    # wrap off the edges
    def edges(self):
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width
            
        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height
    
    
    
    # align this boid with all the other boids within a perception radius
    def align(self, boids):
        perception_radius = 40
        total = 0
        average = PVector(0, 0) # this is our desired velocity
        
        # find the average of the velocities of all the boids
        for boid in boids:
            distance = PVector.dist(self.position, boid.position)
            # only calculate within a desired perception radius
            if boid != self and distance < perception_radius:
                total += 1 # count how many are within our radius to divide later for average
                average.add(boid.velocity)                
        
        steering_force = average
        
        if total > 0:
            steering_force.div(total) # this is our desired velocity!
            # a steering force = desired velocity - actual velocity, 
            # kind of like correcting error
            
            steering_force.setMag(self.max_speed)
            steering_force = PVector.sub(steering_force, self.velocity)
            steering_force.limit(self.max_force)
        # else:            
        #     # note that if we didn't find anything, we return the zero vector
        #     return PVector(0, 0)
     
 
        return steering_force
        
        
    def flock(self, boids):
        alignment = self.align(boids)
        self.acceleration.add(alignment) 

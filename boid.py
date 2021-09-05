
# an automated bird! kind of like a bird and droid
class Boid:
    def __init__(self):
        self.position = PVector(random(width), random(height))
        self.velocity = PVector().random2D().setMag(random(0.5, 1.5))
        self.acceleration = PVector()
        self.max_force = random(0.15, 0.25)
        self.max_speed = random(2.5, 4.5)
        self.ACC_VECTOR_SCALE = 200
        self.r = 16


    # update the boid's position, velocity, and acceleration
    def update(self):
        self.velocity.add(self.acceleration)
        self.position.add(self.velocity)
        self.velocity.limit(self.max_speed)
        self.acceleration.mult(0)
    
                        
    # draw the acceleration vector    
    # TODO: add arrow
    def show_acc_vector(self):
        pushMatrix()
        translate(self.position.x, self.position.y)
        stroke(200, 100, 100, 50)
        strokeWeight(2)
        line(0, 0, self.ACC_VECTOR_SCALE*self.acceleration.x, self.ACC_VECTOR_SCALE*self.acceleration.y)
        noStroke()    
        popMatrix()
        print self.acceleration.mag()
        

    def show(self):
        # self.show_acc_vector()
        # rotate the object to point where its velocity vector points        
        pushMatrix()
        translate(self.position.x, self.position.y)
        
        # draw vel vector
        VEL_VECTOR_SCALE = 10
        stroke(0, 100, 100, 50)
        strokeWeight(1)
        # velocity vector isn't useful because vehicles rotate in that direction
        # line(0, 0, VEL_VECTOR_SCALE*self.vel.x, VEL_VECTOR_SCALE*self.vel.y)
        noStroke()
        
        # rotate 
        rotate(self.velocity.heading())
        
        # this is where we draw our object. we're going to try for a 9S Hackbot
        # https://puu.sh/I3E19/9d32002c25.png
        r = self.r
        
        T = 0.4 # how far away is the tip away from the origin?
        C = 0.2 # what is the radius of the inner circle?
        B = 0.3 # how far away is the butt away from the origin?
        
        fill(0, 0, 100, 75)
        stroke(0, 0, 0, 100)
        strokeWeight(1)
        beginShape()
        vertex(r, 0) # front tip
        vertex(0, r*T) # top
        vertex(-r*T, 0) # butt
        vertex(0, -r*T) # bottom
        vertex(r, 0) # front tip
        endShape()
        
        fill(0, 0, 0, 90)
        circle(0, 0, r*C)
        stroke(0, 0, 0, 100)
        strokeWeight(1)
        line(0, 0, -r*T, 0) # line to the butt
        
        x = (r*T)/(sqrt(3)+T)
        line(0, 0, x, sqrt(3)*x) # line to the top 120 degrees
        line(0, 0, x, -sqrt(3)*x) # line to the bottom 120 degrees
        
        # two little squares in the back
        rectMode(CENTER)
        fill(0, 0, 100, 50)
        strokeWeight(1)
        square(r*-B, r*T, r*0.2)
        square(r*-B, -r*T, r*0.2)        
        rectMode(CORNER)
        popMatrix()
        # draw the velocity vector? unnecessary because we rotate to that direction
 
 
    def show_simple(self):
        strokeWeight(4)
        stroke(0, 0, 100)
        fill(0, 0, 100, 50)
        point(self.position.x, self.position.y)
        
    
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
 
 
    def apply_force(self, force):
        # F=ma, but we assure m=1 so our force vector becomes an acceleration vector
        self.acceleration.add(force)
        
 
    # steering force = desired velocity - current velocity, as per Craig Reynolds's
    # sbfac paper. Desired velocity should be a vector with direction toward where we
    # want to go. Our steering force acts like a correction; it corrects for our current
    # velocity and steers us to cancel that and toward our target 
    #
    # returns a force vector steering this boid to its target's position
    def seek_target(self, target_position):
        # a vector pointing from us to our target, which we will treat as a velocity
        # instead of the position it actually is
        desired_velocity = PVector.sub(target_position, self.position)
        return self.seek_velocity(desired_velocity)
    
    
    # this needs to be called with a desired velocity
    # as per Craig Reynolds's paper, steering force = desired velocity - current velocity
    # seek calls this with PVector.sub(target_position, self.position) 
    #
    # returns a force vector steering this boid toward its provided desired velocity
    def seek_velocity(self, desired_velocity):
        # set this velocity to our max speed
        desired_velocity.setMag(self.max_speed)
        
        # steering force = desired velocity - current velocity
        # note that we are taking a velocity vector and are going to treat it as an
        # acceleration vector :o
        steering = PVector.sub(desired_velocity, self.velocity)
        steering.limit(self.max_force)
        return steering
        
        
    
    def evade(self, target_position):
        return self.seek(target_position).mult(-1)
        
    
    # try to steer toward the same heading as neighboring boids within a perception radius
    # this implementation uses seek!
    # returns a zero force PVector if there are no other boids within a radius
    def align(self, boids, perception_radius):
        total = 0 # total number of neighboring boids we use for calculating the avg heading
        average = PVector() # this vector will hold the average heading of neighboring boids
        
        # find the average heading of neighboring boids
        for boid in boids:
            distance = PVector.dist(self.position, boid.position)
            # only calculate for other boids (not us!) within the radius
            if boid != self and distance < perception_radius:
                total += 1
                average.add(boid.velocity) # velocity contains heading information
        
        if total > 0:
            average.div(total)       
            return self.seek_velocity(average)
        else:
            return PVector()    


    # steer to move toward the average location of nearby flockmates
    def cohesion(self, boids, perception_radius):
        total = 0
        average = PVector(0, 0) # this is our desired velocity
        
        # find the average of the positions of all the boids
        for boid in boids:
            distance = PVector.dist(self.position, boid.position)
            
            # only calculate within a desired perception radius
            if boid != self and distance < perception_radius:
                total += 1 # count how many are within our radius to divide later for average
                
                # in self.align, we added the other boids' velocities. here we add position!
                average.add(boid.position)                
        
        steering_force = average
        
        if total > 0:
            steering_force.div(total) # this is our desired velocity!
    
            # note that we subtract our position from the average position first;
            # this is the main difference from self.align!                    
            return self.seek_target(steering_force)            
            
        # # note that if we didn't find anything, we return the zero vector
        return PVector(0, 0)
    
    
    # applies flock behaviors to all boids
    def flock(self, boids):
        alignment = self.align(boids, 40)
        self.acceleration.add(alignment)
        
        cohesion = self.cohesion(boids, 40) 
        self.acceleration.add(cohesion)
        
        separation = self.separation(boids, 30)
        self.acceleration.add(separation)        
    
    
    # steer to avoid crowding local flockmates
    def separation(self, boids, perception_radius):
        total = 0
        average = PVector(0, 0) # this is our desired velocity
        
        # find the average of the positions of all the boids
        for boid in boids:
            distance = PVector.dist(self.position, boid.position)
            
            # only calculate within a desired perception radius
            if boid != self and distance < perception_radius:
                difference = PVector.sub(self.position, boid.position)
                # we want this difference to be inversely proportional to the distance between
                # self and other; the further away it is, the lower the magnitude we want
                
                # TODO: fix zero division error
                difference.div(distance)                
                total += 1 # count how many are within our radius to divide later for average
                
                # in self.align, we added the other boids' velocities. here we add position!
                average.add(difference)                
        
        steering_force = average
        
        if total > 0:
            steering_force.div(total) # this is our desired velocity!        
            return self.seek_velocity(steering_force).mult(1.5)            
            
        # # note that if we didn't find anything, we return the zero vector
        return PVector(0, 0)

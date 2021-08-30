class Point:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data # store the object this point represents, i.e. Particle, Boid
        
    def __repr__(self):
        return "({},{})".format(self.x, self.y)
        

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        print(self)
    
    # test if this contains a point
    def contains(self, p):
        # we're using the same inclusion as python's range: [a, b)
        # this makes it so the center of each quadtree isn't shared
        # but is also guaranteed to belong to the se boundary
        # the above is no longer true
        
        # BUG currently inserting points at (width, height) only inserts 1/4 of the time
        # resolved! this was because of integer division during subdivide
        return (p.x >= self.x) and (p.x <= self.x+self.w) and (p.y >= self.y) and (p.y <= self.y+self.h)


    # do we intersects with another rectangle?
    def intersects(self, target):
        # there are eight cases for intersection; we can reduce the computation time by 
        # finding the four cases that fail intersection and taking a logical NOT
        return not (
                (self.x > target.x + target.w) or 
                (self.y > target.y + target.h) or 
                (target.x > self.x + self.w) or 
                (target.y > self.y + self.h))
    
    
    def __repr__(self):
        s = "I am a rectangle at point {},{} with width {} and height {}"
        return s.format(self.x, self.y, self.w, self.h)        

class Quadtree():
    def __init__(self, boundary, n): # boundary is a Rectangle
        self.boundary = boundary
        
        # how big is the quadtree? when do I need to subdivide? 
        # this is a job for capacity
        self.capacity = n
        
        # stores the list of points in this quadtree only, but not its children
        self.points = []
        
        # have we divided once yet?
        self.divided = False


    def insert(self, p): # p is a Point
        if not self.boundary.contains(p):
            return False;
        
        if len(self.points) < self.capacity:
            self.points.append(p)
            return True;
        else:
            if not self.divided:
                self.subdivide()
            
            # this trainwreck hopefully guarantees that we don't have duplicate points lol
            # when a point is on the edge of a boundary, the priority queue is: {nw, ne, se, sw}
            # spoilers: this does not work
            if self.northwest.insert(p):
                return True
            elif self.northeast.insert(p):
                return True
            elif self.southeast.insert(p):
                return True
            elif self.southwest.insert(p):
                return True
    
    
    def __repr__(self):
        # return "I'm a quadtree with capacity {}".format(self.capacity)
        return str(self.points)
        
            
    # we will split into 4 subsections: nw, ne, sw, se
    def subdivide(self):        
        # local variables to make code more readable
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h        
        
        nw = Rectangle(x, y, w/2.0, h/2.0)
        ne = Rectangle(x+w/2.0, y, w/2.0, h/2.0)
        sw = Rectangle(x, y+h/2.0, w/2.0, h/2.0)
        se = Rectangle(x+w/2.0, y+h/2.0, w/2.0, h/2.0)
        
        self.northeast = Quadtree(ne, self.capacity)
        self.northwest = Quadtree(nw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)
        
        self.divided = True
    
    
    def count(self):
        # if self.northwest exists, then all the other 3 quadrants will also exist
        # because they are only created together. love, Cody
        # oops lol, we already have a self.divided that we can use for this
        if self.divided:
            return len(self.points) + self.northwest.count() + self.northeast.count() + self.southwest.count() + self.southeast.count()
        else:
            return len(self.points)
        
        
    # return a list of points within a boundary
    # an aabb is an axis-aligned bounding box, aka rectangle
    def query(self, aabb):
        found = [] # 
        
        # if there's no intersectsion, we don't need to do any work :3
        if not self.boundary.intersects(aabb):
            pass 
        else:
            # look through all points of this quadtree
            for p in self.points:
                if aabb.contains(p):
                    found.append(p)
            
            # recurse through all of our children and ask them if they can find points in target_boundary
            if self.divided:
                found += self.northwest.query(aabb)
                found += self.northeast.query(aabb)
                found += self.southwest.query(aabb)
                found += self.southeast.query(aabb)
        
        # return an empty array if we don't intersects and find nothing
        # otherwise return the result of recursion
        return found
            
    
    
    # return a list of points in this quadtree
    # TODO: not sure why [:] doesn't work. copy() is in Python3 only too ; ;
    def point_list(self):
            
        p = self.points[:]
        
        if self.divided:
            nw = self.northwest.point_list()[:]
            ne = self.northeast.point_list()[:]
            sw = self.southwest.point_list()[:]
            se = self.southeast.point_list()[:]
            
            return p.extend(nw.extend(ne.extend(se.extend(sw))))
        else:
            return p
    
    
    def show(self):
        stroke(0, 0, 100, 100)
        noFill()
        rect(self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h)
        
        if self.divided: # checking existence
            self.northwest.show()
            self.northeast.show()
            self.southeast.show()
            self.southwest.show()

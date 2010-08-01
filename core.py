from math import pi, sqrt
import Image
import colorsys

# -------------------------------------------------------
#
# Definitions for masking feature
#
# -------------------------------------------------------

def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class Mask:
    def contains(self, x, y):
        raise TypeError("Must be implemented in subclass")

class CircleMask(Mask):
    def __init__(self, x, y, radius, reverse=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.reverse = reverse
    
    def contains(self, px, py):
        result = (distance(px, py, self.x, self.y) < self.radius)
        if self.reverse:
            return not result
        else:
            return result

# -------------------------------------------------------
#
# Definitions for image loading, saving, and manipulation
#
# -------------------------------------------------------
class InImage:
    def __init__(self, filename):
        self.inim = Image.open(filename)
        self.nx, self.ny = self.inim.size
        self.inmat = self.inim.load()
        self.w, self.h = self.inim.size
        
    def __getitem__(self, (x, y)):
        return self.inmat[x % self.nx, y % self.ny]
        
    def all_coords(self):
        for y in xrange(self.ny):
            for x in xrange(self.nx):
                yield x, y
                
class OutImage:
    def __init__(self, in_image):
        self.nx, self.ny = in_image.nx, in_image.ny
        self.outim = in_image.inim.copy()
        self.outmat = self.outim.load()
        
    def __setitem__(self, (x, y), value):
        self.outmat[x % self.nx, y % self.ny] = value
        
    def save(self, filename, *args, **kwds):
        self.outim.save(filename, *args, **kwds)


# -------------------------------------------------------
#
# Core analysis routine
#
# -------------------------------------------------------

def run_analysis(filename, scale_factor, fuel, masks=[]):
    
    print "Loading image."
    m1 = InImage(filename)
    m2 = OutImage(m1)
    
    print "Filtering for pellets"
    # Create map of HSL to coordinates
    h_coord = {}
    l_coord = {}
    s_coord = {}
    for x, y in m1.all_coords():
    
        # if point in mask, don't add it
        skip = reduce(lambda acc, cur: acc or cur, [mask.contains(x, y) for mask in masks], False)    
        if skip:
            continue
    
        hls = colorsys.rgb_to_hls(*[a/255.0 for a in m1[x, y]])
    
        H = int(hls[0] * 360.0)    
        L = int(hls[1] * 100.0)
        S = int(hls[2] * 100.0)
    
        hh = h_coord.get(H, [])
        hh.append((x, y))
        h_coord[H] = hh
        
        ll = l_coord.get(L, [])
        ll.append((x, y))
        l_coord[L] = ll

        ss = s_coord.get(S, [])
        ss.append((x, y))
        s_coord[S] = ss

    # Color masked pixels black
    for x, y in m1.all_coords():
        masked = reduce(lambda acc, cur: acc or cur, [mask.contains(x, y) for mask in masks], False)    
        if masked:
            m2[x, y] = (0, 0, 0)

    # Filter based on hue and saturation
    def filter_range(source, lo, hi):    
        res = []
        for x in range(lo, hi):
            res.extend(source.get(x, []))
        return set(res)    
    
    pellet_hue_coords = filter_range(h_coord, fuel["PELLET_LOWER"], fuel["PELLET_UPPER"])
    high_sat_coords = filter_range(s_coord, fuel["LOW_SAT"], fuel["HIGH_SAT"])
    pellet_coords = pellet_hue_coords.intersection(high_sat_coords)
    
    number_pixels = len(pellet_coords)

    # Color the pixels in the output image red
    for x, y in pellet_coords:
        m2[x, y] = (255, 0, 0)
        
    print "Saving results"
    m2.save("results.png")
    
    print "-----------------------------------"
    area_pixel = scale_factor * scale_factor
    
    print "Number of pixels counted: %s" % number_pixels
    print "Area of pixel: %f cm^2" % area_pixel
    print "Area of unburned pellets: %f cm^2" % (number_pixels * area_pixel)
    print "Mass of unburned pellets: %f g" % (number_pixels * area_pixel * fuel["area_to_mass"])
    
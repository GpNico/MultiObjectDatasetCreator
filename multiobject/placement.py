"""
Store multiple functions that dictate the placements of 
objects in the picture that are to be called by base.py
"""
import numpy as np

def random_place(x, obj_size):
    """
        Place objects randomly on the image.
    """
    r = np.random.randint(x.shape[0] - obj_size[0] + 1)
    c = np.random.randint(x.shape[1] - obj_size[1] + 1)
    
    return r, c
  
def center_place(x, obj_size):
    """
        Place objects at the center of the image.
    """
    r = (x.shape[0] - obj_size[0])//2
    c = (x.shape[1] - obj_size[1])//2
    
    return r, c
    
def xalign_place(x, obj_size):
    """
        Place objects on the line y = 0.
    """
    r = (x.shape[0] - obj_size[0])//2
    c = np.random.randint(x.shape[1] - obj_size[1] + 1)
    
    return r, c
    
def yalign_place(x, obj_size):
    """
        Place objects on the line y = 0.
    """
    r = np.random.randint(x.shape[0] - obj_size[0] + 1)
    c = (x.shape[1] - obj_size[1])//2
    
    return r, c
    
    
    
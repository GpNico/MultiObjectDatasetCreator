import numpy as np
import multiobject.placement as plc
from utils import get_rela_code, get_rela_list, get_placement_func

class Placer:
    
    def __init__(self, n_sprites, attribute_names, sprites_attr, allow_overlap, sprites, noise):
        #Get attributes
        self.n_sprites = n_sprites
        self.attribute_names = attribute_names
        self.sprites_attr = sprites_attr
        self.allow_overlap = allow_overlap
        self.sprites = sprites
        self.noise = noise
        
        #Possible relations
        self.rela_2_obj, self.rela_3_obj = get_rela_list()
        #Relations functions
        self.relations_func = get_placement_func()
        #Relations code
        self.relations_code = get_rela_code()
        
        
    def place(self, relation):
        assert (relation in self.rela_2_obj) or (relation in self.rela_3_obj)
        
        if relation in self.rela_2_obj:
            placement = self.relations_func[relation]
            x, image_labels, fail_flag = self._place_2_obj(placement, add_noise = self.noise)
            image_labels['relation'] = self.relations_code[relation]
        elif relation in self.rela_3_obj:
            placement1, placement2, switch = self.relations_func[relation]
            x, image_labels, fail_flag = self._place_3_obj(placement1, placement2, add_noise = self.noise, switch = switch)
            image_labels[-1] = self.relations_code[relation]
            
        return x, image_labels, fail_flag
        
    def update_x(self, x):
        self.x = x
              
    def _place_2_obj(self, placement, add_noise = False):
        
        im_size_r, im_size_c, _ = self.x.shape
        
        num_obj = 2
        
        image_labels = {k: [] for k in self.attribute_names}
        
        # Pick the sprite type for each objects in this image
        random_obj_types = np.random.choice(range(self.n_sprites), size=num_obj, replace=True)
        
        # Locations containing rendered sprites
        occupied = np.zeros_like(self.x, dtype='uint8')
        
        # Dictionary with (key=attribute name, value=list of attribute values
        # for each object in this image)
        image_labels = {k: [] for k in self.attribute_names}

        curr_attempts = 0   # current attempts to place objects
        
        obj_count = 0
        
        # FIRST OBJECT 
        #random
        obj_type_1 = random_obj_types[obj_count]
        obj_scale_1 = self.sprites_attr['scale'][obj_type_1]
        obj_angle_1 = self.sprites_attr['angle'][obj_type_1]
        vertices1 = self.sprites_attr['vertices'][obj_type_1]

        patch_size_1 = self.sprites[obj_type_1].shape
        obj_size_1 = [int(patch_size_1[0]*obj_scale_1), int(patch_size_1[1]*obj_scale_1), patch_size_1[2]]
        
        r_1 = np.random.randint(self.x.shape[0] - patch_size_1[0] + 1)
        c_1 = np.random.randint(self.x.shape[1] - patch_size_1[1] + 1)
        
        #place the object
        occupied[r_1:r_1 + patch_size_1[0], c_1:c_1 + patch_size_1[1]] = 1
        
        # Render entity by adding and clipping
        sprite_1 = self.sprites[obj_type_1]
        self.x[r_1:r_1 + patch_size_1[0], c_1:c_1 + patch_size_1[1]] += sprite_1
        self.x = np.clip(self.x, a_min=0, a_max=255)
        
        
        # Increment object counter
        obj_count += 1
        
        # SECOND OBJECT
        obj_type_2 = random_obj_types[obj_count]
        obj_scale_2 = self.sprites_attr['scale'][obj_type_2]
        obj_angle_2 = self.sprites_attr['angle'][obj_type_2]
        vertices2 = self.sprites_attr['vertices'][obj_type_2]

        patch_size_2 = self.sprites[obj_type_2].shape
        obj_size_2 = [int(patch_size_2[0]*obj_scale_2), int(patch_size_2[1]*obj_scale_2), patch_size_2[2]]
        
        while curr_attempts < 100:
            try:
                kwargs = {'r_1':r_1, 'c_1':c_1, 'obj_size_1':obj_size_1, 'obj_size_2':obj_size_2,'x_shape':self.x.shape, 'vertices1': vertices1, 'vertices2': vertices2}
                r_2, c_2 = placement(**kwargs)
               
                curr_attempts += 1
                overlap = np.count_nonzero(occupied[r_2:r_2 + patch_size_2[0], c_2:c_2 + patch_size_2[1]]) > 0
                if overlap and not self.allow_overlap:
                    continue
                else:
                    
                    occupied[r_2:r_2 + patch_size_2[0], c_2:c_2 + patch_size_2[1]] = 1

                    # Render entity by adding and clipping
                    sprite_2 = self.sprites[obj_type_2]
                    self.x[r_2:r_2 + patch_size_2[0], c_2:c_2 + patch_size_2[1]] += sprite_2
                    self.x = np.clip(self.x, a_min=0, a_max=255)
                    
                    break
            except:
                curr_attempts += 1
        
        fail_flag = False
        if curr_attempts >= 100:
            fail_flag = True
        if not(fail_flag):    
            for k in self.attribute_names:
                if k == 'coords':
                    image_labels[k].append([r_1/im_size_r, c_1/im_size_c])
                    image_labels[k].append([r_2/im_size_r, c_2/im_size_c])
                elif k == 'relation':
                    pass
                else:    
                    image_labels[k].append(self.sprites_attr[k][obj_type_1])
                    image_labels[k].append(self.sprites_attr[k][obj_type_2])
            
            if add_noise:
                image_labels = self._add_noise(occupied, image_labels, max_obj = 2)

        return self.x, image_labels, fail_flag
        
    
        
        
    def _add_noise(self, occupied, image_labels, max_obj = 2):
        im_size_r, im_size_c, _ = self.x.shape
        
        req_n_obj = np.random.randint(max_obj + 1)
        
        random_obj_types = np.random.choice(range(self.n_sprites), size=req_n_obj, replace=True)
        
        curr_attempts = 0 # current attempts to place objects
        obj_count = 0
        while True:
            # Reached required number of objects
            if obj_count == req_n_obj:
                break

            # Hard limit, just drop sample at this point and try again
            if curr_attempts > 100:
                break

            obj_type = random_obj_types[obj_count]
            obj_size = self.sprites[obj_type].shape
            r = np.random.randint(self.x.shape[0] - obj_size[0] + 1)
            c = np.random.randint(self.x.shape[1] - obj_size[1] + 1)
            curr_attempts += 1
            overlap = np.count_nonzero(
                occupied[r:r + obj_size[0], c:c + obj_size[1]]) > 0
            if overlap: #and not self.allow_overlap:
                continue
            occupied[r:r + obj_size[0], c:c + obj_size[1]] = 1

            # Render entity by adding and clipping
            sprite = self.sprites[obj_type]
            self.x[r:r + obj_size[0], c:c + obj_size[1]] += sprite
            self.x = np.clip(self.x, a_min=0, a_max=255)

            # Increment object counter
            obj_count += 1

            for k in self.attribute_names:
                if k == 'coords':
                    image_labels[k].append([r/im_size_r, c/im_size_c])
                elif k == 'relation':
                    pass
                else:    
                    image_labels[k].append(self.sprites_attr[k][obj_type])

        return image_labels
        
        
        
        
        
        
        
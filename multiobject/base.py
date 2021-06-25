import numpy as np
from tqdm import tqdm
import multiobject.placement as plc
import multiobject.placer as placer
import multiobject.exhaustivator as exhaustivator


def generate_multiobject_dataset(n, shape, sprites, sprites_attr, allow_overlap=False, count_rela = None, noise = True):


    assert len(shape) == 3, "the image shape should be (height, width, channels)"
    probsum_rela = sum(count_rela.values())
    #assert abs(probsum_rela - 1.0) < 1e-6, "count of relation probabilities must sum to 1"
    bgr = np.zeros(shape, dtype='int')
    color_channels = shape[-1]
    n_sprites = len(sprites)
    print("num sprites: {}".format(n_sprites))

    # Names of object attributes
    attribute_names = list(sprites_attr.keys()) + ['coords', 'relation'] #shape, angle, color, scale, coords

    # Generated images
    images = []

    labels = {k: [] for k in attribute_names}

    #counts_rela = {rela: int(np.ceil(v * n)) for rela, v in count_rela.items()}
    counts_rela = count_rela
    relations = list(counts_rela.keys())

    for sprite in sprites:
        # Check sprite shape
        msg = ("each sprite should have shape (height, width, channels), "
               "found sprite with shape {}".format(sprite.shape))
        assert sprite.ndim == 3, msg
        msg = "sprites channels ({}) should be the same as background " \
              "channels ({}))".format(sprite.shape[-1], color_channels)
        assert color_channels == sprite.shape[-1], msg
        
        
    Placer = placer.Placer(n_sprites, attribute_names, sprites_attr, allow_overlap, sprites, noise=noise)

    Exhaustivator = exhaustivator.Exhaustivator(count_rela, shape)

    #relations_idx = len(relations) - 1
    rela_idx_to_construct = [i for i in range(len(relations))]

    generated_imgs = 0
    fail_count = 0
    progress_bar = tqdm()
    while True:

        # Reached required number of images
        if (np.array(list(counts_rela.values()))<=0).all():
            break
        relations_idx = np.random.choice(rela_idx_to_construct)
        rela = relations[relations_idx]

        if counts_rela[rela] <= 0:
            rela_idx_to_construct.remove(relations_idx)
            continue
        
        #background
        x = bgr.copy()
        
        Placer.update_x(x)
        
        #Place sprites according to this relation
        x, image_labels, fail_flag = Placer.place(rela)
          
        if fail_flag:
            fail_count += 1
            if fail_count >= 10*n:
                raise Exception("Maximum number of fails reached !")
            continue
        else:
            #Time to exhaustivate !!
            Y, counts_rela = Exhaustivator.exhaustivate(image_labels['coords'], image_labels['vertices'], counts_rela)
            image_labels['relation'] = Y

        # Append image, number of objects in it, and each object's attributes
        images.append(x.astype('uint8'))
        #counts_rela[rela] -= 1
        for k in attribute_names:
            labels[k].append(np.array(image_labels[k]))

        generated_imgs += 1
        progress_bar.update()
    progress_bar.close()

    images = np.stack(images, axis=0)

    perm = np.random.permutation(len(images))  # indices
    images = images[perm]
    for k in attribute_names:
        labels[k] = [labels[k][i] for i in perm]
    
    print("Count of Relations Created : ", Exhaustivator.rela_count)

    return images, labels

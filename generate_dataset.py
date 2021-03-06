import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from multiobject import generate_multiobject_dataset
from sprites import generate_dsprites, generate_binary_mnist
from utils import get_date_str, show_img_grid, color_name, readable_labels, get_rela_list, get_rela_code, get_params, parse_args

supported_sprites = ['dsprites', 'binary_mnist']

def main():

    args = parse_args()

    ### SETTINGS #############################
    n = args.data_size   # num images
    frame_size = (args.frame_size, args.frame_size)
    patch_size = args.patch_size

    gpu_acceleration = args.gpu

    N_rela = n
    

                  
    #count_rela = {'right': 0*N_rela//4, 'left': 0*N_rela//4, 'top': 0*N_rela//4, 'below': 0*N_rela//4,
     #             'contact_right': N_rela, 'contact_left': N_rela, 'contact_on': N_rela, 'contact_below': N_rela}
    
    #count_rela = {'right': N_rela//2, 'left': N_rela//2, 'contact_on': N_rela, 'contact_below': N_rela}

    count_rela = {'top': N_rela//2, 'below': N_rela//2, 'contact_right': N_rela, 'contact_left': N_rela}

    allow_overlap = args.overlap
    ##########################################
    

    # Generate sprites and labels
    print("generating sprites...")
    if args.dataset_type == 'dsprites':
        sprites, labels, shape_dict = generate_dsprites(patch_size)
    elif args.dataset_type == 'binary_mnist':
        sprites, labels = generate_binary_mnist(patch_size)
    elif args.dataset_type == 'clevr':
        print('You have chosen clevr congrats !!')
        if gpu_acceleration:
            print("GPU Accelerated !")
            os.system('blender --background --python image_generation/render_images.py -- --num_images {} --use_gpu 1'.format(N_rela))
        else:
            print("No GPU available or CUDA 10.x installed !")
            os.system('blender --background --python image_generation/render_images.py -- --num_images {}'.format(N_rela))
        exit()
    else:
        raise NotImplementedError

    
    # Create dataset
    print("generating dataset...")
    ch = sprites[0].shape[-1]
    img_shape = (*frame_size, ch)
    dataset, labels = generate_multiobject_dataset(
        n, img_shape, sprites, labels,
        allow_overlap=allow_overlap,
        count_rela = count_rela,
        noise = args.noise)
    print("done")
    print("shape:", dataset.shape)
    
    rela_code = get_rela_code()
    rela_2, rela_3 = get_rela_list()

    #labels['text'] = readable_labels(labels, rela_code, rela_2, rela_3, shape_dict)
    print("Labels keys ", labels.keys())

    # Save dataset
    print("saving...")
    
    root = os.path.join('generated', args.folder)
    os.makedirs(root, exist_ok=True)
    fname = 'multi_' + args.dataset_type + '_' + args.file
    fname = os.path.join(root, fname)
    np.savez_compressed(fname, x=dataset, labels=labels)
    
    print('done')




if __name__ == '__main__':
    main()

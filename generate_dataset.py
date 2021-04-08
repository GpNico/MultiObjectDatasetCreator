import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from multiobject import generate_multiobject_dataset
from sprites import generate_dsprites, generate_binary_mnist
from utils import get_date_str, show_img_grid

supported_sprites = ['dsprites', 'binary_mnist']

def main():

    args = parse_args()

    ### SETTINGS #############################
    n = args.data_size   # num images
    frame_size = (args.frame_size, args.frame_size)
    patch_size = args.patch_size

    # count_distrib = {1: 1}
    count_distrib = {0: 1/3, 1: 1/3, 2: 1/3}
    allow_overlap = args.overlap
    ##########################################


    # Generate sprites and labels
    print("generating sprites...")
    if args.dataset_type == 'dsprites':
        sprites, labels = generate_dsprites(patch_size)
    elif args.dataset_type == 'binary_mnist':
        sprites, labels = generate_binary_mnist(patch_size)
    else:
        raise NotImplementedError

    """
    # Show sprites
    show_img_grid(8, sprites, random_selection=True,
                  fname='gen_{}_sprites.png'.format(get_date_str()))
    """
    
    # Create dataset
    print("generating dataset...")
    ch = sprites[0].shape[-1]
    img_shape = (*frame_size, ch)
    dataset, n_obj, labels = generate_multiobject_dataset(
        n, img_shape, sprites, labels,
        count_distrib=count_distrib,
        allow_overlap=allow_overlap,
        place = args.place)
    print("done")
    print("shape:", dataset.shape)

    # Number of objects is part of the labels
    labels['n_obj'] = n_obj
    

    # Save dataset
    print("saving...")
    
    root = os.path.join('generated', args.folder)
    os.makedirs(root, exist_ok=True)
    fname = 'multi_' + args.dataset_type + '_' + args.file
    fname = os.path.join(root, fname)
    np.savez_compressed(fname, x=dataset, labels=labels)
    
    print('done')
    
    """
    # Show samples and print their attributes
    print("\nAttributes of saved samples:")
    show_img_grid(4, dataset, labels,
                  fname='gen_{}_images.png'.format(get_date_str()))

    # Show distribution of number of objects per image
    plt.figure()
    plt.hist(n_obj, np.arange(min(n_obj) - 0.5, max(n_obj) + 0.5 + 1, 1))
    plt.title("Distribution of num objects per image")
    plt.xlabel("Number of objects")
    plt.savefig('gen_{}_distribution.png'.format(get_date_str()))
    """

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False)
    
    parser.add_argument('--type',
                        type=str,
                        default='dsprites',
                        metavar='NAME',
                        dest='dataset_type',
                        help="dataset type")
    parser.add_argument('--folder',
                        type=str,
                        default='custom',
                        dest='folder',
                        help='output folder')
    parser.add_argument('--file',
                        type=str,
                        default=get_date_str(),
                        dest='file',
                        help='file name')
    parser.add_argument('-n',
                        type=int,
                        default=10,
                        dest='data_size',
                        help='dataset size')
    parser.add_argument('--frame_size',
                        type=int,
                        default=64,
                        dest='frame_size',
                        help='frame size')
    parser.add_argument('--patch_size',
                        type=int,
                        default=18,
                        dest='patch_size',
                        help='patch size')
    parser.add_argument('--overlap',
                        type=bool,
                        default=True,
                        dest='overlap',
                        help='allow overlap')
    parser.add_argument('-p',
                        '--placement',
                        type=str,
                        default='random',
                        dest='place',
                        help='Chose the placement of the objects. For now : random, center, xalign, yalign')
                        
    args = parser.parse_args()
    #Check if data type is supported
    if args.dataset_type not in supported_sprites:
        raise NotImplementedError(
            "unsupported dataset '{}'".format(args.dataset_type))
            
    #Create output folder if needed
    folders = os.listdir('generated/')
    if args.folder not in folders:
        os.mkdir('generated/' + args.folder)
        
    # Check if placement option is correct
    supported_place = ['random', 'center', 'xalign', 'yalign']
    if args.place not in supported_place:
        raise NotImplementedError(
            "unsupported placement '{}'".format(args.place))
            
            
    return args


if __name__ == '__main__':
    main()

import numpy as np
import yaml
from importlib import import_module
import argparse
import os

supported_sprites = ['dsprites', 'binary_mnist']

def color_name(arr):
    assert arr.shape[0] == 3, "Color array must be of shapr 3"
    
    x, y, z = arr
    
    if x == 255:
        if y == 0 and z == 0:
            return 'red'
        elif y == 255 and z == 0:
            return 'yellow'
        elif y == 255 and z == 255:
            return 'white'
        elif y == 0 and z == 255:
            return 'magenta'
    elif x == 0:
        if y == 255 and z == 0:
            return 'green'
        elif y == 255 and z == 255:
            return 'cyan'
        elif y == 0 and z == 255:
            return 'blue'
    else:
        return 'weird color'
        
def import_from_path(path_to_module, obj_name = None):
    module_name = path_to_module.replace("/",".").strip(".py")
    module = import_module(module_name)
    if obj_name == None:
        return module
    obj = getattr(module, obj_name)
    return obj
        
        
def get_rela_code(config_name = 'config_1.yml'):
    with open("config/" + config_name) as config_file:
        config = yaml.safe_load(config_file)
        
    rela_code = {}
    
    for rela in config['relations_2_obj']:
        rela_code[rela] = config['relations_2_obj'][rela]['code']
        
    for rela in config['relations_3_obj']:
        rela_code[rela] = config['relations_3_obj'][rela]['code']
        
    return rela_code
    
def get_rela_list(config_name = 'config_1.yml'):
    with open("config/" + config_name) as config_file:
        config = yaml.safe_load(config_file)
        
    rela_list_2_obj, rela_list_3_obj = [], []
    
    for rela in config['relations_2_obj']:
        rela_list_2_obj.append(rela)
        
    for rela in config['relations_3_obj']:
        rela_list_3_obj.append(rela)
        
    return rela_list_2_obj, rela_list_3_obj
    
    
def get_placement_func(config_name = 'config_1.yml'):
    with open("config/" + config_name) as config_file:
        config = yaml.safe_load(config_file)
        
    rela_func = {}
    
    for rela in config['relations_2_obj']:
        rela_func[rela] = import_from_path('multiobject/placement.py' , obj_name = str(config['relations_2_obj'][rela]['placement']))
        
    for rela in config['relations_3_obj']:
        rela_func[rela] = [import_from_path('multiobject/placement.py' , obj_name = str(config['relations_3_obj'][rela]['placement1'])),
                           import_from_path('multiobject/placement.py' , obj_name = str(config['relations_3_obj'][rela]['placement2'])),
                           bool(int(config['relations_3_obj'][rela]['switch']))]
    
    return rela_func
    
def readable_labels(labels, rela_code, rela_2, rela_3, shape_dict):
    #relations dict
    rela_dict = {v: k for k, v in rela_code.items()}
    
    label_dict = {'relation': [], 'text': [], 'brut': []}
    
    #readble labels
    for k in range(len(labels)):
        label = labels[k]
        rela = rela_dict[label[-1]]
        if rela in rela_2:
            read_lab = color_name(label[3]) + ' ' + shape_dict[label[2]] + ' ' + rela + ' \n ' + color_name(label[1]) + ' ' + shape_dict[label[0]]
            label_dict['relation'].append(label[-1]) 
            label_dict['text'].append(read_lab)
            label_dict['brut'].append(label)
        elif rela in rela_3:
            if rela == 'aligned':
                read_lab = color_name(label[1]) + ' ' + shape_dict[label[0]] + ', '
                read_lab += color_name(label[3]) + ' ' + shape_dict[label[2]] + ', \n'
                read_lab += color_name(label[5]) + ' ' + shape_dict[label[4]] + ' ' + rela
                labels[k] = [label, read_lab]
            elif rela == 'A_right_B_B_left_C':
                read_lab = color_name(label[1]) + ' ' + shape_dict[label[0]] + ' right '
                read_lab += color_name(label[3]) + ' ' + shape_dict[label[2]] + ', \n which is left '
                read_lab += color_name(label[5]) + ' ' + shape_dict[label[4]]
                labels[k] = [label, read_lab]
            elif rela == 'A_right_B_A_top_C':
                read_lab = color_name(label[1]) + ' ' + shape_dict[label[0]] + ' right '
                read_lab += color_name(label[3]) + ' ' + shape_dict[label[2]] + ', \n and top '
                read_lab += color_name(label[5]) + ' ' + shape_dict[label[4]]
                labels[k] = [label, read_lab]                
            else:
                read_lab = 'unkown ternary relations'
                labels[k] = [label, read_lab]
            
    return label_dict
    
def get_params(config_name = 'config_1.yml'):
    with open("config/" + config_name) as config_file:
        config = yaml.safe_load(config_file)
        
    return config['params']
    
    
def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False)
        
    config = get_params()
    
    parser.add_argument('--type',
                        type=str,
                        default=config['type'],
                        metavar='NAME',
                        dest='dataset_type',
                        help="dataset type")
    parser.add_argument('--folder',
                        type=str,
                        default=config['folder'],
                        dest='folder',
                        help='output folder')
    parser.add_argument('--file',
                        type=str,
                        default=config['file'],
                        dest='file',
                        help='file name')
    parser.add_argument('-n',
                        type=int,
                        default=config['n'],
                        dest='data_size',
                        help='dataset size')
    parser.add_argument('--frame_size',
                        type=int,
                        default=config['frame_size'],
                        dest='frame_size',
                        help='frame size')
    parser.add_argument('--patch_size',
                        type=int,
                        default=config['patch_size'],
                        dest='patch_size',
                        help='patch size')
    parser.add_argument('--overlap',
                        type=int,
                        default=config['overlap'],
                        dest='overlap',
                        help='allow overlap : : 0 = False, 1 = True')
    parser.add_argument('--noise',
                        type=int,
                        default=config['noise'],
                        dest='noise',
                        help='allow noise : 0 = False, 1 = True')
                        
    args = parser.parse_args()
    #Check if data type is supported
    if args.dataset_type not in supported_sprites:
        raise NotImplementedError(
            "unsupported dataset '{}'".format(args.dataset_type))
            
    #Create output folder if needed
    folders = os.listdir('generated/')
    if args.folder not in folders:
        os.mkdir('generated/' + args.folder)
        
    if args.overlap == 0:
        args.overlap = False
    else:
        args.overlap = True
        
    if args.noise == 0:
        args.noise = False
    else:
        args.noise = True
            
            
    return args
    
    
    
    
    
    
    
    
    
    
    
    
    
    

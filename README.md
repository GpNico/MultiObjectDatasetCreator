# MultiObjectDatasetCreator

This repo has been created in the context of an internship at LSCP on Attention Mechanism. The goal is to create a Multi Object Dataset with respect to instructions on how objects should be placed. For example we wish to automate the creation of images where the label could be "the cube is on the right of the triangle" or "the circle is more to the right than at the top of the diamond". The overall idea is to investigate whether or not a deep attention mechanism can learn more easily natural relationship between objects, in the sense that the word that describes this relation exists in the human language.

## Important

This work is based on the original codes for creation of Binarized MNIST, dSprites and CLEVR datasets. We just added novels commands and modified the way objects are placed.

Multi-object datasets : https://github.com/addtt/multi-object-datasets

CLEVR Dataset Generation : https://github.com/facebookresearch/clevr-dataset-gen

## How to use

More on that once the code is usable !

## Requirements

For now :
- Python 3
- numpy
- matplotlib
- scikit_image
- tqdm
- pillow

Optional :
- torch
- torchvision

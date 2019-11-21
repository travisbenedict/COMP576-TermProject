import os
import random
import glob
import numpy as np
import shutil


def split_folder(data_dir, train_pct, val_pct):
    """
    Given a directory containing images and their masks create a new directory which has directories for 
    test, validation and test sets. NOTE: 0 < train_pct + val_pct < 1
    :param data_dir: The directory holding the data
    :param train_pct: The percentage of the data to use for training
    :param val_pct: The percentage of data to use for validation
    """

    random.seed(1)

    IMG_SUFFIX = '*_sat.jpg'
    MASK_SUFFIX = '*_msk.png'

    glob_imgs = os.path.join(data_dir,IMG_SUFFIX)
    glob_masks = os.path.join(data_dir, MASK_SUFFIX)

    img_paths = np.array(glob.glob(glob_imgs))
    mask_paths = np.array(glob.glob(glob_masks))

    num_imgs = len(img_paths)
    index_lst = list(range(num_imgs))

    random.shuffle(index_lst)

    train_idx_bound = int(train_pct * num_imgs)
    train_imgs = img_paths[index_lst[:train_idx_bound]]
    train_masks = mask_paths[index_lst[:train_idx_bound]]

    val_idx_bound = int((train_pct + val_pct) * num_imgs)
    val_imgs = img_paths[index_lst[train_idx_bound: val_idx_bound]]
    val_masks = mask_paths[index_lst[train_idx_bound: val_idx_bound]]

    test_imgs = img_paths[index_lst[val_idx_bound:]]
    test_masks = mask_paths[index_lst[val_idx_bound:]]

    # Write the lists to their own directories
    copy_list_to_dir(train_imgs, "train")
    copy_list_to_dir(train_masks, "train")
    copy_list_to_dir(val_imgs, "val")
    copy_list_to_dir(val_masks, "val")
    copy_list_to_dir(test_imgs, "test")
    copy_list_to_dir(test_masks, "test")


def copy_list_to_dir(file_list, subdir,  dir="NewData"):
    """
    Given a list of file names copy them to a new directory
    :param file_list: A list of file names to move 
    :param subdir: The sub directory of dir to put the files in
    :param dir: The main directory for putting files in
    """

    subdir = os.path.join(dir, subdir)

    if not os.path.exists(dir):
        os.mkdir(dir)

    if not os.path.exists(subdir):
        os.mkdir(subdir)

    for file in file_list:
        base_name = os.path.basename(file)
        shutil.copy(base_name, os.path.join(subdir, base_name))

    print("Moved files into: ", subdir)


if __name__ == "__main__":
    split_folder("data/train", 0.7, 0.15)






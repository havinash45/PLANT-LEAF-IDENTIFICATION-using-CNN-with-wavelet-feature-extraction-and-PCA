"""
One-time script: Keep only 20 images per class subfolder in dataset.
Deletes the rest.
Run from project root: python trim_dataset_to_25.py
"""
import os
import random

DATASET_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG', '.bmp', '.BMP'}
KEEP_COUNT = 15  # 20 images per subfolder


def get_paths_to_scan():
    paths = []
    leaf_base = os.path.join(DATASET_ROOT, 'leaf_dataset')
    if os.path.isdir(leaf_base):
        for sub in ['images', 'segmented']:
            sub_path = os.path.join(leaf_base, sub)
            if os.path.isdir(sub_path):
                for subsub in ['lab', 'field']:
                    p = os.path.join(sub_path, subsub)
                    if os.path.isdir(p):
                        paths.append(p)
    pv_base = os.path.join(DATASET_ROOT, 'plantvillage dataset')
    if os.path.isdir(pv_base):
        for sub in ['color', 'grayscale', 'segmented']:
            p = os.path.join(pv_base, sub)
            if os.path.isdir(p):
                paths.append(p)
    return paths


def trim_folder(folder_path):
    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f))
             and os.path.splitext(f)[1] in IMAGE_EXTENSIONS]
    if len(files) <= KEEP_COUNT:
        return 0
    to_keep = random.sample(files, KEEP_COUNT)
    to_remove = [f for f in files if f not in to_keep]
    deleted = 0
    for f in to_remove:
        try:
            os.remove(os.path.join(folder_path, f))
            deleted += 1
        except Exception as e:
            print(f"  Error deleting {f}: {e}")
    return deleted


def main():
    paths = get_paths_to_scan()
    if not paths:
        print("No dataset paths found.")
        return
    total_deleted = 0
    for base_path in paths:
        if not os.path.isdir(base_path):
            continue
        rel_base = os.path.relpath(base_path, DATASET_ROOT)
        for folder_name in sorted(os.listdir(base_path)):
            folder_path = os.path.join(base_path, folder_name)
            if not os.path.isdir(folder_path):
                continue
            n = trim_folder(folder_path)
            if n > 0:
                total_deleted += n
                print(f"  {rel_base}/{folder_name}: kept {KEEP_COUNT}, deleted {n}")
    print(f"Done. Total images deleted: {total_deleted}")


if __name__ == '__main__':
    main()

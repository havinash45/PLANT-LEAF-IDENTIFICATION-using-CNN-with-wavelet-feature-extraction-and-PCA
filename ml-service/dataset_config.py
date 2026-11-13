"""
Dynamic dataset configuration for plant identification training.
Scans dataset folder for leaf_dataset and plantvillage dataset structures.
Folder names become class labels - fully dynamic.
"""
import os

# Dataset root - sibling to ml-service (project root/dataset)
def get_dataset_root():
    """Returns path to dataset folder (project root/dataset)."""
    ml_service_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(ml_service_dir)
    return os.path.join(project_root, 'dataset')

def get_dataset_paths(dataset_root=None):
    """
    Returns list of (base_path, sub_paths) for each dataset structure.
    Each sub_path leads to directories containing plant/class folders with images.
    
    leaf_dataset:
      - images/lab, images/field
      - segmented/lab, segmented/field
    
    plantvillage dataset:
      - color, grayscale, segmented (each has plant folders directly)
    """
    if dataset_root is None:
        dataset_root = get_dataset_root()
    
    paths_to_scan = []
    
    # Leaf dataset: dataset/leaf_dataset/images/lab, images/field, segmented/lab, segmented/field
    leaf_base = os.path.join(dataset_root, 'leaf_dataset')
    if os.path.isdir(leaf_base):
        for sub in ['images', 'segmented']:
            sub_path = os.path.join(leaf_base, sub)
            if os.path.isdir(sub_path):
                for subsub in ['lab', 'field']:
                    p = os.path.join(sub_path, subsub)
                    if os.path.isdir(p):
                        paths_to_scan.append(p)
    
    # PlantVillage: dataset/plantvillage dataset/color, grayscale, segmented
    pv_base = os.path.join(dataset_root, 'plantvillage dataset')
    if os.path.isdir(pv_base):
        for sub in ['color', 'grayscale', 'segmented']:
            p = os.path.join(pv_base, sub)
            if os.path.isdir(p):
                paths_to_scan.append(p)
    
    return paths_to_scan

def discover_all_classes(dataset_root=None):
    """
    Scan all dataset paths and return:
    - class_to_index: dict mapping class_name -> index
    - image_paths: list of (full_path, class_index)
    """
    paths = get_dataset_paths(dataset_root)
    if not paths:
        return {}, [], []
    
    class_names = []  # ordered list
    class_to_index = {}
    image_paths = []  # (path, class_index)
    
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG', '.bmp', '.BMP'}
    
    for base_path in paths:
        if not os.path.isdir(base_path):
            continue
        for folder_name in sorted(os.listdir(base_path)):
            folder_path = os.path.join(base_path, folder_name)
            if not os.path.isdir(folder_path):
                continue
            # Folder name = class name (e.g., acer_campestre, Tomato___Late_blight)
            class_name = folder_name
            if class_name not in class_to_index:
                class_to_index[class_name] = len(class_names)
                class_names.append(class_name)
            
            class_idx = class_to_index[class_name]
            for fname in os.listdir(folder_path):
                ext = os.path.splitext(fname)[1]
                if ext in IMAGE_EXTENSIONS:
                    full_path = os.path.join(folder_path, fname)
                    image_paths.append((full_path, class_idx))
    
    return class_to_index, image_paths, class_names

"""
Dynamic Plant Identification Training Script
Trains on leaf_dataset + plantvillage dataset - all folders become classes.
Fully dynamic: add new datasets by extending dataset_config.py.

Usage:
    python train_model.py
    python train_model.py --epochs 30 --batch_size 32
    python train_model.py --data_dir ../dataset  # custom dataset root
"""

import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
import random

from dataset_config import get_dataset_root, discover_all_classes

IMG_SIZE = 224
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG', '.bmp', '.BMP'}


class PlantDataGenerator(keras.utils.Sequence):
    """Custom generator that loads images from scattered dataset paths."""
    
    def __init__(self, image_paths, class_indices, batch_size=32, img_size=IMG_SIZE, augment=False, shuffle=True):
        self.image_paths = image_paths  # list of (path, class_idx)
        self.batch_size = batch_size
        self.img_size = img_size
        self.augment = augment
        self.shuffle = shuffle
        self.indices = np.arange(len(image_paths))
        if shuffle:
            np.random.shuffle(self.indices)
    
    def __len__(self):
        return int(np.ceil(len(self.image_paths) / self.batch_size))
    
    def __getitem__(self, idx):
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        X_batch = []
        y_batch = []
        
        for i in batch_indices:
            path, class_idx = self.image_paths[i]
            try:
                img = load_img(path, target_size=(self.img_size, self.img_size))
                arr = img_to_array(img)
                if arr.shape[2] == 1:
                    arr = np.concatenate([arr] * 3, axis=-1)
                elif arr.shape[2] == 4:
                    arr = arr[:, :, :3]
                arr = arr / 255.0
                if self.augment:
                    arr = self._augment(arr)
                X_batch.append(arr)
                y_batch.append(class_idx)
            except Exception as e:
                pass  # skip corrupted images
        
        if not X_batch:
            return self.__getitem__((idx + 1) % self.__len__())
        
        X = np.array(X_batch)
        y = keras.utils.to_categorical(y_batch, num_classes=self.num_classes)
        return X, y
    
    def _augment(self, img):
        if np.random.random() > 0.5:
            img = np.fliplr(img)
        if np.random.random() > 0.5:
            img = np.flipud(img)
        return img
    
    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)
    
    def set_num_classes(self, n):
        self.num_classes = n


def create_model(num_classes):
    """Transfer learning with MobileNetV2 - lightweight, production-ready."""
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    return Model(inputs=base_model.input, outputs=predictions)


def train(data_dir=None, epochs=30, batch_size=32, validation_split=0.2, model_save_path=None, sample_ratio=1.0):
    """
    Train plant identification model on all discovered datasets.
    """
    dataset_root = data_dir or get_dataset_root()
    
    print("=" * 60)
    print("Dynamic Plant Identification Training")
    print("=" * 60)
    print(f"Dataset root: {dataset_root}")
    
    class_to_index, image_paths, class_names = discover_all_classes(dataset_root)
    
    if not image_paths:
        print("ERROR: No images found in dataset folder!")
        print("Expected structure:")
        print("  dataset/leaf_dataset/images/lab|field/<plant_folder>/images")
        print("  dataset/leaf_dataset/segmented/lab|field/<plant_folder>/images")
        print("  dataset/plantvillage dataset/color|grayscale|segmented/<plant_folder>/images")
        exit(1)
    
    num_classes = len(class_names)
    print(f"Classes found: {num_classes}")
    print(f"Total images: {len(image_paths)}")
    
    if sample_ratio < 1.0:
        n_keep = max(int(len(image_paths) * sample_ratio), num_classes * 5)
        random.shuffle(image_paths)
        image_paths = image_paths[:n_keep]
        print(f"Using sample: {len(image_paths)} images (ratio={sample_ratio})")
    
    print(f"Sample classes: {class_names[:5]}...")
    
    # Train/val split (stratify when possible for balanced splits)
    random.seed(42)
    np.random.seed(42)
    paths_with_idx = [(p, c) for p, c in image_paths]
    labels = [c for _, c in paths_with_idx]
    try:
        train_paths, val_paths = train_test_split(
            paths_with_idx, test_size=validation_split,
            random_state=42, stratify=labels
        )
    except ValueError:
        train_paths, val_paths = train_test_split(
            paths_with_idx, test_size=validation_split, random_state=42
        )
    
    print(f"Train samples: {len(train_paths)}, Val samples: {len(val_paths)}")
    
    train_gen = PlantDataGenerator(train_paths, None, batch_size=batch_size, augment=True, shuffle=True)
    train_gen.set_num_classes(num_classes)
    
    val_gen = PlantDataGenerator(val_paths, None, batch_size=batch_size, augment=False, shuffle=False)
    val_gen.set_num_classes(num_classes)
    
    model = create_model(num_classes)
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nTraining started...")
    history = model.fit(
        train_gen,
        epochs=epochs,
        validation_data=val_gen,
        verbose=1
    )
    
    # Save model
    if model_save_path is None:
        model_save_path = os.path.join(os.path.dirname(__file__), 'models', 'plant_classifier.h5')
    
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    model.save(model_save_path)
    
    # Save class names
    class_names_path = os.path.join(os.path.dirname(model_save_path), 'class_names.txt')
    with open(class_names_path, 'w', encoding='utf-8') as f:
        for name in class_names:
            f.write(f"{name}\n")
    
    print("\n" + "=" * 60)
    print(f"Model saved: {model_save_path}")
    print(f"Class names: {class_names_path}")
    print(f"Final train accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final val accuracy: {history.history['val_accuracy'][-1]:.4f}")
    print("=" * 60)
    
    return model, class_names


if __name__ == '__main__':
    default_data_dir = get_dataset_root()
    default_model_path = os.path.join(os.path.dirname(__file__), 'models', 'plant_classifier.h5')
    
    parser = argparse.ArgumentParser(description='Train plant identification model (dynamic - all datasets)')
    parser.add_argument('--data_dir', type=str, default=default_data_dir,
                        help='Path to dataset root (contains leaf_dataset, plantvillage dataset)')
    parser.add_argument('--epochs', type=int, default=30, help='Training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--validation_split', type=float, default=0.2, help='Validation split ratio')
    parser.add_argument('--model_save_path', type=str, default=default_model_path,
                        help='Where to save trained model')
    parser.add_argument('--sample_ratio', type=float, default=1.0,
                        help='Use fraction of data for quick testing (e.g. 0.1 = 10%%)')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.data_dir):
        print(f"Error: Dataset directory not found: {args.data_dir}")
        exit(1)
    
    train(args.data_dir, args.epochs, args.batch_size, args.validation_split, args.model_save_path, args.sample_ratio)

import os
import shutil
import random
from PIL import Image
from config import *

def create_output_dirs(classes):
    """Create train/val/test folders for each class."""
    for split in [PROCESSED_TRAIN, PROCESSED_VAL, PROCESSED_TEST]:
        for cls in classes:
            os.makedirs(os.path.join(split, cls), exist_ok=True)
    print(" Output folders created.")

def is_valid_image(path):
    """Check if file is a valid, openable image."""
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except:
        return False

def resize_and_save(src_path, dst_path):
    """Resize image to 224x224 and save."""
    with Image.open(src_path) as img:
        img = img.convert("RGB")
        img = img.resize(IMAGE_SIZE)
        img.save(dst_path)

def split_and_process(source_dir, tag=""):
    """
    Reads class folders from source_dir,
    splits into train/val/test and saves processed images.
    tag = label prefix e.g. 'pdoc_' for PlantDoc to avoid name clashes
    """
    classes = [
        d for d in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, d))
    ]
    print(f"\n📂 Found {len(classes)} classes in {source_dir}")
    create_output_dirs(classes)

    total_saved = 0
    skipped     = 0

    for cls in classes:
        cls_path = os.path.join(source_dir, cls)
        images   = [
            f for f in os.listdir(cls_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        # Filter corrupt images
        valid_images = [
            f for f in images
            if is_valid_image(os.path.join(cls_path, f))
        ]
        skipped += len(images) - len(valid_images)

        random.seed(RANDOM_SEED)
        random.shuffle(valid_images)

        # Calculate split indices
        n        = len(valid_images)
        n_test   = max(1, int(n * TEST_SPLIT))
        n_val    = max(1, int(n * VAL_SPLIT))
        n_train  = n - n_test - n_val

        splits = {
            PROCESSED_TRAIN : valid_images[:n_train],
            PROCESSED_VAL   : valid_images[n_train:n_train + n_val],
            PROCESSED_TEST  : valid_images[n_train + n_val:]
        }

        for split_dir, filenames in splits.items():
            for fname in filenames:
                src = os.path.join(cls_path, fname)
                # Add tag prefix to filename to avoid clashes between datasets
                dst_fname = f"{tag}{fname}"
                dst = os.path.join(split_dir, cls, dst_fname)
                try:
                    resize_and_save(src, dst)
                    total_saved += 1
                except Exception as e:
                    print(f"  ⚠️  Skipping {fname}: {e}")
                    skipped += 1

        print(f"  ✅ {cls}: {n_train} train | {n_val} val | {n_test} test")

    print(f"\n🎉 Done! Total saved: {total_saved} | Skipped/corrupt: {skipped}")

def process_plantdoc():
    """
    PlantDoc already has train/test split.
    We process each separately and merge into our structure.
    """
    print("\n🌿 Processing PlantDoc dataset...")
    for subset in ["train", "test"]:
        subset_dir = os.path.join(PLANTDOC_DIR, subset)
        if not os.path.exists(subset_dir):
            print(f"    {subset} folder not found in PlantDoc, skipping.")
            continue
        # Map PlantDoc test → our test, PlantDoc train → our train+val
        if subset == "test":
            # Copy directly to processed test
            classes = [
                d for d in os.listdir(subset_dir)
                if os.path.isdir(os.path.join(subset_dir, d))
            ]
            create_output_dirs(classes)
            for cls in classes:
                cls_path = os.path.join(subset_dir, cls)
                images = [
                    f for f in os.listdir(cls_path)
                    if f.lower().endswith((".jpg", ".jpeg", ".png"))
                ]
                for fname in images:
                    src = os.path.join(cls_path, fname)
                    dst = os.path.join(PROCESSED_TEST, cls, f"pdoc_{fname}")
                    if is_valid_image(src):
                        try:
                            resize_and_save(src, dst)
                        except Exception as e:
                            print(f"    {fname}: {e}")
        else:
            split_and_process(subset_dir, tag="pdoc_")

if __name__ == "__main__":
    print("=" * 50)
    print("  PlantDocBot — Image Preprocessing Pipeline")
    print("=" * 50)

    # Process PlantVillage (direct class folders)
    print("\n🌱 Processing PlantVillage dataset...")
    split_and_process(PLANTVILLAGE_DIR, tag="pv_")

    # Process PlantDoc (has train/test subfolders)
    process_plantdoc()

    print("\n All datasets preprocessed and saved to data/processed/")
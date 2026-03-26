import os
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from config import *

# ── GPU Memory Growth (prevents crash on some systems) ──
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

def create_data_generators():
    """Create train, val, test data generators."""

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        PROCESSED_TRAIN,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )

    val_generator = val_test_datagen.flow_from_directory(
        PROCESSED_VAL,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    test_generator = val_test_datagen.flow_from_directory(
        PROCESSED_TEST,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    return train_generator, val_generator, test_generator

def build_model(num_classes):
    """Build MobileNetV2 transfer learning model."""

    # Load MobileNetV2 without top layer
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )

    # Freeze base model layers first
    base_model.trainable = False

    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.4)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    output = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model, base_model

def plot_history(history, save_path):
    """Plot and save training curves."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(history.history['accuracy'],     label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()

    ax2.plot(history.history['loss'],     label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Val Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(save_path)
    print(f" Training curves saved to {save_path}")

def evaluate_model(model, test_generator):
    """Evaluate model on test set."""
    print("\n🔍 Evaluating on test set...")
    loss, accuracy = model.evaluate(test_generator)
    print(f"  Test Loss     : {loss:.4f}")
    print(f"  Test Accuracy : {accuracy * 100:.2f}%")

    # Detailed classification report
    y_pred = model.predict(test_generator)
    y_pred_classes = y_pred.argmax(axis=1)
    y_true = test_generator.classes
    class_names = list(test_generator.class_indices.keys())

    print("\n📋 Classification Report:")
    print(classification_report(y_true, y_pred_classes, target_names=class_names))

if __name__ == "__main__":
    print("=" * 55)
    print("   PlantDocBot — CNN Disease Classification Training")
    print("=" * 55)

    # Create saved_models dir
    os.makedirs(MODELS_DIR, exist_ok=True)

    # ── Step 1: Load Data ────────────────────────────────
    print("\n📂 Loading datasets...")
    train_gen, val_gen, test_gen = create_data_generators()
    num_classes = len(train_gen.class_indices)
    print(f"   Classes found : {num_classes}")
    print(f"   Train samples : {train_gen.samples}")
    print(f"   Val samples   : {val_gen.samples}")
    print(f"   Test samples  : {test_gen.samples}")

    # ── Step 2: Build Model ──────────────────────────────
    print("\n Building MobileNetV2 model...")
    model, base_model = build_model(num_classes)
    model.summary()

    # ── Step 3: Phase 1 Training (frozen base) ───────────
    print("\n Phase 1: Training classification head...")
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            CNN_MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            verbose=1
        )
    ]

    history1 = model.fit(
        train_gen,
        epochs=15,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )

    # ── Step 4: Phase 2 Fine-tuning (unfreeze top layers) 
    print("\n Phase 2: Fine-tuning top layers...")
    base_model.trainable = True

    # Freeze all layers except last 30
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    # Recompile with lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    history2 = model.fit(
        train_gen,
        epochs=10,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )

    # ── Step 5: Evaluate ─────────────────────────────────
    evaluate_model(model, test_gen)

    # ── Step 6: Save training curves ─────────────────────
    plot_path = os.path.join(MODELS_DIR, "training_curves.png")
    plot_history(history2, plot_path)

    print(f"\n Model saved to: {CNN_MODEL_PATH}")
    print(" CNN Training Complete!")
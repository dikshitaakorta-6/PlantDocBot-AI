import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from config import *

# ── Load saved model ────────────────────────────────────
print("venv\Scripts\activate Loading saved model...")
model = tf.keras.models.load_model(CNN_MODEL_PATH)

# ── Data generators ─────────────────────────────────────
val_test_datagen = ImageDataGenerator(rescale=1./255)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

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

# ── Callbacks ────────────────────────────────────────────
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=3,
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
        patience=2,
        verbose=1
    )
]

# ── Resume fine-tuning ───────────────────────────────────
print("\n🔧 Resuming fine-tuning for 3 remaining epochs...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00005),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_generator,
    epochs=3,
    validation_data=val_generator,
    callbacks=callbacks,
    verbose=1
)

# ── Final Evaluation ─────────────────────────────────────
print("\n🔍 Final evaluation on test set...")
loss, accuracy = model.evaluate(test_generator)
print(f"  Test Accuracy : {accuracy * 100:.2f}%")
print(f"   Test Loss     : {loss:.4f}")
print(f"\n Done! Model saved to: {CNN_MODEL_PATH}")
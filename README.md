<div align="center">

# 🍎 Apple & Orange Classifier 🍊

### Image Classification Using Convolutional Neural Networks

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white" alt="Keras">
  <img src="https://img.shields.io/badge/Computer%20Vision-00599C?style=for-the-badge" alt="Computer Vision">
  <img src="https://img.shields.io/badge/Deep%20Learning-8A2BE2?style=for-the-badge" alt="Deep Learning">
</p>

### 🎯 96% Test Accuracy

**An educational deep learning project that classifies images of apples and oranges using a custom-built CNN architecture.**

</div>

---

## 📌 Overview

This project implements an image classification system using a **Convolutional Neural Network (CNN)** built with TensorFlow and Keras.

The primary objective is to train a deep learning model capable of distinguishing between two fruit categories:

- 🍎 **Apple** — Class 0
- 🍊 **Orange** — Class 1

The project includes model development, image classification, evaluation on unseen test data, and real-time prediction using a webcam.

It also serves as a foundation for future experiments with advanced CNN architectures and Transfer Learning.

---

## ✨ Features

- 🧠 Custom CNN architecture designed from scratch.
- 🍎 Binary image classification: Apple vs. Orange.
- 📊 Dataset splitting into training, validation, and testing sets.
- ⚙️ Batch Normalization and Dropout for improved training.
- 📉 Learning Rate Scheduling.
- ⏹️ Early Stopping to prevent unnecessary training.
- 🎥 Real-time image classification using a webcam.
- 📈 Evaluation using Precision, Recall, F1-Score, and Accuracy.
- 🚀 Planned integration with a web application.
- 🔬 Future experimentation with Transfer Learning.

---

## 📂 Dataset

**Dataset Name:** Apple Orange Classifier  
**Source:** Kaggle  
**Total Images:** 796  
**Number of Classes:** 2

### Dataset Distribution

| Class | Label | Number of Images |
|:---|:---:|---:|
| 🍎 Apple | 0 | 396 |
| 🍊 Orange | 1 | 400 |
| **Total** | | **796** |

### Dataset Splitting

The dataset was divided into three subsets:

| Subset | Percentage | Number of Images |
|:---|---:|---:|
| Training | 70% | Approximately 557 |
| Validation | 10% | Approximately 79 |
| Testing | 20% | 160 |
| **Total** | **100%** | **796** |

The test set contains 160 images:

- 75 Apple images
- 85 Orange images

---

## 🖼️ Image Specifications

All images are provided to the CNN with the following specifications:

| Property | Value |
|:---|:---|
| Original Image Size | 128 × 128 pixels |
| Model Input Shape | 128 × 128 × 3 |
| Color Space | RGB |
| Image Format | JPG |
| Preprocessing | No additional preprocessing |

**Note:** No additional image preprocessing operations were applied to the dataset.

---

## 🏗️ CNN Architecture

A custom Convolutional Neural Network was developed for this classification task.

The architecture consists of convolutional layers for feature extraction, pooling layers for spatial dimensionality reduction, and fully connected layers for classification.

### Architecture Components

| Layer Type | Configuration |
|:---|:---|
| Conv2D | 5 layers |
| MaxPooling2D | 3 layers |
| Dense | 2 layers, 256 neurons each |
| Activation | Leaky ReLU |
| Batch Normalization | Used |
| Dropout | Used |
| Output Layer | Dense, 2 neurons |
| Output Activation | Softmax |

### Architecture Details

**1. Convolutional Layers**

Five Conv2D layers are responsible for extracting visual features from the input images, including edges, textures, shapes, and more complex patterns.

**2. Max Pooling Layers**

Three MaxPooling layers reduce the spatial dimensions of feature maps and help decrease computational requirements.

**3. Batch Normalization**

Batch Normalization is used to normalize intermediate activations and help stabilize the training process.

**4. Dropout**

Dropout is applied as a regularization technique to reduce overfitting.

**5. Fully Connected Layers**

Two Dense layers, each containing 256 neurons, process the extracted features before the final classification stage.

**6. Output Layer**

The final Dense layer contains two neurons with Softmax activation, representing the probabilities of the two fruit classes.

---

## ⚙️ Model Training Configuration

The model was trained using the following configuration:

| Parameter | Configuration |
|:---|:---|
| Optimizer | Stochastic Gradient Descent (SGD) |
| Momentum | 0.9 |
| Nesterov Momentum | Enabled |
| Loss Function | Sparse Categorical Crossentropy |
| Batch Size | 32 |
| Training Epochs | Approximately 32 |
| Learning Rate | Dynamic |
| Early Stopping | Enabled |
| Learning Rate Scheduler | Enabled |

### Learning Rate Schedule

A custom learning rate schedule was used during training.

| Epoch Range | Learning Rate |
|:---|---:|
| Epochs 1–2 | 0.001 |
| Epochs 3–10 | 0.01 |
| Epochs 11–50 | 0.001 |

The learning rate changes during training to control the optimization process at different stages.

**Callbacks:**

- **EarlyStopping:** Monitors model performance and stops training when further training is no longer beneficial.
- **LearningRateScheduler:** Dynamically adjusts the learning rate according to the predefined schedule.

---

## 📊 Model Evaluation

The model was evaluated on a separate test dataset containing **160 previously unseen images**.

### Overall Performance

<div align="center">

# 🏆 96% Accuracy

</div>

| Metric | Score |
|:---|---:|
| Test Accuracy | **96%** |
| Macro Precision | 0.96 |
| Macro Recall | 0.95 |
| Macro F1-Score | 0.96 |
| Weighted Precision | 0.96 |
| Weighted Recall | 0.96 |
| Weighted F1-Score | 0.96 |

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|:---|---:|---:|---:|---:|
| 🍎 Apple (0) | 0.97 | 0.93 | 0.95 | 75 |
| 🍊 Orange (1) | 0.94 | 0.98 | 0.96 | 85 |
| **Accuracy** | | | **0.96** | **160** |
| **Macro Avg** | 0.96 | 0.95 | 0.96 | 160 |
| **Weighted Avg** | 0.96 | 0.96 | 0.96 | 160 |

### Performance Analysis

- The model achieved an overall accuracy of approximately 96% on the test dataset.
- Apple classification achieved a precision of 97%.
- Orange classification achieved a recall of 98%.
- The model demonstrated balanced performance across both classes.

**Note:** Training Accuracy, Validation Accuracy, and Test Loss have not been included because their final values were not provided.

---

## 🎥 Real-Time Webcam Classification

In addition to evaluating images from the test dataset, this project includes a real-time classification program using a webcam.

The webcam captures images and passes them to the trained CNN model for prediction.

This allows the model to classify apples and oranges directly from a live camera feed.

---

## 🛠️ Technologies & Libraries

The project was developed using Python and the following libraries:

| Library | Purpose |
|:---|:---|
| TensorFlow | Deep Learning Framework |
| Keras | CNN Model Development |
| NumPy | Numerical Computation |
| Pandas | Data Manipulation |
| Scikit-learn | Dataset Splitting and Evaluation |
| MLxtend | Machine Learning Utilities |
| Matplotlib | Data Visualization |
| Pillow | Image Processing |
| pathlib | File and Directory Management |

---

## 🚀 Future Improvements

This project is an educational foundation for further experiments in Computer Vision and Deep Learning.

Planned improvements include:

- [ ] Experimenting with Transfer Learning.
- [ ] Implementing architectures such as MobileNet, EfficientNet, and VGG.
- [ ] Comparing custom CNN performance against pretrained models.
- [ ] Improving generalization on unseen images.
- [ ] Developing a web-based interface for image classification.
- [ ] Integrating the trained model into a web application.
- [ ] Optimizing inference speed and computational efficiency.

---

## 🎯 Project Goals

The main goal of this project is to gain practical experience with:

- Building CNN architectures from scratch.
- Understanding image classification workflows.
- Training and evaluating deep learning models.
- Applying regularization techniques.
- Working with TensorFlow and Keras.
- Implementing real-time computer vision applications.
- Preparing deep learning models for web integration.

This project is primarily developed for **educational and experimental purposes**.

---

## 👨‍💻 Author

Developed as an educational Computer Vision and Deep Learning project.

**Focus:** CNN, Image Classification, TensorFlow, Keras & Computer Vision.

---

<div align="center">

### 🍎 Built with TensorFlow & Passion for Deep Learning 🍊

**If you find this project interesting, consider giving it a ⭐**

</div>
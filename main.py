from PIL import Image, ImageDraw, ImageFont
import os

# 'a'로 시작하는 단어 리스트
words = [
    "apple", "ant", "anchor", "angle", "arrow", "art", "artist", "atom", "attic", "axis",
]

# 이미지 저장 폴더 생성
if not os.path.exists("word image folder"):
    os.makedirs("word image folder")

# 단어를 이미지로 변환
for word in words:
    # 이미지 크기 및 배경 설정
    img = Image.new('L', (200, 50), color=255)
    draw = ImageDraw.Draw(img)
    
    # 글꼴 설정
    font = ImageFont.truetype("arial.ttf", 24)
    
    # 텍스트 삽입
    draw.text((10, 10), word, font=font, fill=0)
    
    # 파일명 설정 및 저장
    img.save(f"word_images/{word}.png")

######################################################################################################
import glob
from sklearn.model_selection import train_test_split

# 이미지 및 레이블 로드
images = []
labels = []

for filepath in glob.glob("word_images/*_binary.png"):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    images.append(img)
    label = os.path.basename(filepath).split('_')[0]
    labels.append(label)

# numpy 배열로 변환
X = np.array(images)
y = np.array(labels)

# 데이터셋 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

######################################################################################################
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# 모델 정의
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(50, 200, 1)),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(set(y)), activation='softmax')  # 클래스 수에 맞게 설정
])

# 모델 컴파일
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 데이터셋 재구조화
X_train = X_train.reshape(-1, 50, 200, 1)
X_test = X_test.reshape(-1, 50, 200, 1)

# 모델 학습
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))


######################################################################################################
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def predict_missing_letter(image_path):
    # 주어진 이미지를 로드하고 전처리
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    binary_img = binary_img.reshape(1, 50, 200, 1)
    
    # 예측
    predictions = model.predict(binary_img)
    predicted_label = np.argmax(predictions)
    
    # 유사도가 가장 큰 단어 출력
    return y[predicted_label]

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        restored_word = predict_missing_letter(file_path)
        messagebox.showinfo("Restored Word", f"The restored word is: {restored_word}")

# Tkinter 창 생성
root = tk.Tk()
root.title("Word Restoration")

# 버튼 추가
load_button = tk.Button(root, text="Load Image", command=load_image)
load_button.pack()

# Tkinter 이벤트 루프 시작
root.mainloop()

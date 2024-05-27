import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

df = pd.read_csv('english Dictionary.csv')
df.drop_duplicates(subset=['word'], keep = 'last', inplace=True)
df = df.dropna(subset=['word'])
df['word'] = df['word'].astype(str)
df = df[~df['word'].str.contains(r'[^a-zA-Z]')]
df['word'] = df['word'].str.lower()

words = df['word'].tolist()

# 이미지 저장 폴더 생성
if not os.path.exists("word image folder"):
    os.makedirs("word image folder")

# 단어를 이미지로 변환
for word in words:
    if isinstance(word, float):
        continue
    img = Image.new('L', (200, 50), color=255)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 10), word, font=font, fill=0)
    img.save(f"word image folder/{word}.png")
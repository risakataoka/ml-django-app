from django.shortcuts import render, redirect  # 追加
from PIL import Image  # 追加
import numpy as np  # 追加
import base64  # 追加
import tensorflow as tf  # 追加
import os  # 追加
# from tensorflow.keras.models import Sequential  # 追加


# 学習モデルのロード
model = tf.keras.models.load_model('machine/mnist.h5')
model.summary()


def index(request):
    return render(request, 'machine/index.html')


def mnist(input):

    result = model.predict(input).argmax()
    return result


def upload(request):

    # 画像データの取得
    files = request.FILES.getlist("files[]")

    # 簡易エラーチェック（jpg拡張子）
    for memory_file in files:

        root, ext = os.path.splitext(memory_file.name)

        if ext != '.jpg':

            message = "【ERROR】jpg以外の拡張子ファイルが指定されています。"
            return render(request, 'machine/index.html', {
                "message": message,
            })

    if request.method == 'POST' and files:
        result = []
        labels = []
        for file in files:
            img = Image.open(file)
            gray_img = img.convert('L')
            img = gray_img.resize((28, 28))
            img = np.array(img).reshape(1, 28, 28, 1)
            labels.append(mnist(img))

        for file, label in zip(files, labels):
            file.seek(0)
            file_name = file
            src = base64.b64encode(file.read())
            src = str(src)[2:-1]
            result.append((src, label))

        context = {
            'result': result
        }
        return render(request, 'machine/result.html', context)

    else:
        return redirect('index')

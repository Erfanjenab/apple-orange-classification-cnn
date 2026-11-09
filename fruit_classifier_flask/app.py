import os
import io
import numpy as np
from PIL import Image, UnidentifiedImageError
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model

# ---------------- تنظیمات اصلی پروژه ----------------

# مسیر فایل مدل؛ فایل model.keras باید کنار app.py قرار بگیرد.
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.keras")

# نام کلاس‌ها بر اساس ترتیب خروجی مدل:
# در دیتاست شما Apple برابر 0 و Orange برابر 1 است.
CLASS_NAMES = ["Apple", "Orange"]

# اگر هنگام آموزش تصاویر را بر 255 تقسیم کرده‌اید، این مقدار باید True باشد.
# اگر هنگام آموزش این کار را نکرده‌اید، مقدار را False کنید.
NORMALIZE_PIXELS = True

# حداکثر حجم فایل آپلودی: 8 مگابایت
MAX_FILE_SIZE = 8 * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# ---------------- بارگذاری مدل فقط یک‌بار ----------------

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"فایل مدل پیدا نشد: {MODEL_PATH}\n"
        "فایل model.keras را کنار app.py قرار دهید."
    )

# مدل هنگام شروع سرور بارگذاری می‌شود تا برای هر درخواست دوباره لود نشود.
model = load_model(MODEL_PATH)

# اندازه ورودی مدل از خود مدل خوانده می‌شود.
# برای مدل‌های تصویری معمولاً شکل ورودی به صورت (None, height, width, 3) است.
input_shape = model.input_shape
if isinstance(input_shape, list):
    input_shape = input_shape[0]

if len(input_shape) != 4 or input_shape[-1] not in (3, None):
    raise ValueError(
        f"مدل باید ورودی تصویری RGB با شکل (None, height, width, 3) داشته باشد؛ "
        f"شکل فعلی: {input_shape}"
    )

# اگر ابعاد ورودی مدل مشخص باشد، همان ابعاد استفاده می‌شود.
# در صورت داینامیک بودن ابعاد، مقدار پیش‌فرض 224 در نظر گرفته می‌شود.
IMG_HEIGHT = int(input_shape[1]) if input_shape[1] is not None else 224
IMG_WIDTH = int(input_shape[2]) if input_shape[2] is not None else 224

print(f"مدل با موفقیت بارگذاری شد. ورودی مورد انتظار: {input_shape}")
print(f"اندازه تصاویر برای پیش‌بینی: {IMG_WIDTH}x{IMG_HEIGHT}")

# ---------------- توابع پردازش تصویر ----------------

def preprocess_image(file_bytes):
    """
    بایت‌های تصویر آپلودشده را دریافت می‌کند و:
    1) تصویر را با Pillow باز می‌کند.
    2) آن را به RGB تبدیل می‌کند.
    3) اندازه را مطابق ورودی مدل تغییر می‌دهد.
    4) به آرایه NumPy تبدیل می‌کند.
    5) در صورت نیاز مقادیر پیکسل را بین صفر و یک می‌برد.
    6) یک بُعد batch به ابتدای آرایه اضافه می‌کند.
    """

    # باز کردن تصویر از حافظه؛ نیازی به ذخیره دائمی فایل روی دیسک نیست.
    image = Image.open(io.BytesIO(file_bytes))

    # تبدیل تصاویر خاکستری، RGBA و سایر حالت‌ها به RGB سه‌کاناله
    image = image.convert("RGB")

    # تغییر اندازه دقیقاً مطابق ابعاد ورودی مدل
    image = image.resize((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.BILINEAR)

    # تبدیل تصویر به آرایه عددی با شکل (height, width, 3)
    image_array = np.asarray(image, dtype=np.float32)

    # این مرحله باید با پیش‌پردازش زمان آموزش مدل یکسان باشد.
    if NORMALIZE_PIXELS:
        image_array = image_array / 255.0

    # اضافه کردن batch dimension:
    # از (H, W, 3) به (1, H, W, 3)
    image_array = np.expand_dims(image_array, axis=0)

    return image_array


# ---------------- مسیرهای سایت ----------------

@app.route("/")
def index():
    # نمایش صفحه اصلی سایت
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # بررسی اینکه اصلاً فایلی ارسال شده است یا نه
    if "image" not in request.files:
        return jsonify({"error": "هیچ تصویری ارسال نشده است."}), 400

    uploaded_file = request.files["image"]

    if uploaded_file.filename == "":
        return jsonify({"error": "ابتدا یک تصویر انتخاب کنید."}), 400

    try:
        # خواندن فایل آپلودشده به صورت بایت
        file_bytes = uploaded_file.read()

        if not file_bytes:
            return jsonify({"error": "فایل انتخاب‌شده خالی است."}), 400

        # پردازش تصویر و آماده‌سازی ورودی مدل
        processed_image = preprocess_image(file_bytes)

        # اجرای پیش‌بینی مدل
        prediction = model.predict(processed_image, verbose=0)
        prediction = np.asarray(prediction)

        # این پروژه بر اساس مدل دوکلاسه Softmax طراحی شده است.
        # خروجی مورد انتظار: [[احتمال Apple، احتمال Orange]]
        probabilities = prediction[0].astype(float)

        if probabilities.size != 2:
            return jsonify({
                "error": (
                    "خروجی مدل دو مقدار ندارد. این کد برای مدل دوکلاسه "
                    "با خروجی Softmax نوشته شده است."
                )
            }), 500

        # تبدیل خروجی به درصد برای نمایش در رابط کاربری
        # اگر خروجی مدل Softmax باشد مجموع این دو مقدار تقریباً 1 است.
        # نرمال‌سازی زیر از خطاهای کوچک عددی جلوگیری می‌کند.
        total = float(np.sum(probabilities))
        if total <= 0:
            return jsonify({"error": "خروجی مدل معتبر نیست."}), 500

        probabilities = probabilities / total

        # انتخاب کلاسی که احتمال بیشتری دارد
        predicted_index = int(np.argmax(probabilities))
        predicted_class = CLASS_NAMES[predicted_index]
        confidence = float(probabilities[predicted_index]) * 100

        return jsonify({
            "class_name": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": {
                "Apple": round(float(probabilities[0]) * 100, 2),
                "Orange": round(float(probabilities[1]) * 100, 2)
            }
        })

    except (UnidentifiedImageError, OSError):
        return jsonify({"error": "فایل ارسال‌شده یک تصویر معتبر نیست."}), 400
    except Exception as error:
        # خطای واقعی در ترمینال ثبت می‌شود؛ جزئیات فنی به کاربر نمایش داده نمی‌شود.
        app.logger.exception("خطا هنگام پیش‌بینی تصویر")
        return jsonify({"error": "هنگام پردازش تصویر خطایی رخ داد."}), 500


# ---------------- اجرای برنامه ----------------

if __name__ == "__main__":
    # debug=True فقط برای توسعه محلی مناسب است؛ برای انتشار عمومی خاموش شود.
    app.run(host="127.0.0.1", port=5000, debug=True)

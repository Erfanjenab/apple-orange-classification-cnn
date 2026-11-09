// ---------------- گرفتن عناصر مورد نیاز از صفحه ----------------
const imageInput = document.getElementById("imageInput");
const dropZone = document.getElementById("dropZone");
const browseButton = document.getElementById("browseButton");
const changeImageButton = document.getElementById("changeImageButton");
const tryAgainButton = document.getElementById("tryAgainButton");

const uploadPrompt = document.getElementById("uploadPrompt");
const previewContent = document.getElementById("previewContent");
const imagePreview = document.getElementById("imagePreview");
const resultImage = document.getElementById("resultImage");

const resultCard = document.getElementById("resultCard");
const loading = document.getElementById("loading");
const statusMessage = document.getElementById("statusMessage");

let selectedFile = null;
let previewUrl = null;

// ---------------- باز کردن پنجره انتخاب فایل ----------------
function openFilePicker() {
    imageInput.click();
}

browseButton.addEventListener("click", (event) => {
    // جلوگیری از اجرای هم‌زمان کلیک روی والد
    event.stopPropagation();
    openFilePicker();
});

changeImageButton.addEventListener("click", openFilePicker);
dropZone.addEventListener("click", (event) => {
    // کلیک روی خود باکس یا محتوای آن پنجره انتخاب فایل را باز می‌کند.
    if (event.target.closest("button")) return;
    openFilePicker();
});

// ---------------- مدیریت Drag & Drop ----------------
["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.add("drag-over");
    });
});

["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.remove("drag-over");
    });
});

dropZone.addEventListener("drop", (event) => {
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        handleSelectedFile(files[0]);
    }
});

// ---------------- دریافت فایل از input ----------------
imageInput.addEventListener("change", () => {
    if (imageInput.files.length > 0) {
        handleSelectedFile(imageInput.files[0]);
    }
});

// ---------------- بررسی و نمایش پیش‌نمایش فایل ----------------
function handleSelectedFile(file) {
    // فقط فرمت‌های تصویری مورد قبول را می‌پذیریم.
    const allowedTypes = ["image/jpeg", "image/png"];

    if (!allowedTypes.includes(file.type)) {
        showError("فرمت فایل باید JPG یا PNG باشد.");
        return;
    }

    // محدودیت حجم سمت کاربر برای تجربه بهتر؛ محدودیت اصلی در Flask هم بررسی می‌شود.
    if (file.size > 8 * 1024 * 1024) {
        showError("حجم تصویر نباید بیشتر از 8 مگابایت باشد.");
        return;
    }

    selectedFile = file;
    clearError();

    // آزاد کردن URL قبلی برای جلوگیری از مصرف بی‌دلیل حافظه
    if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
    }

    previewUrl = URL.createObjectURL(file);
    imagePreview.src = previewUrl;

    document.getElementById("fileName").textContent = file.name;
    document.getElementById("fileSize").textContent =
        (file.size / 1024).toFixed(1) + " KB";

    uploadPrompt.classList.add("hidden");
    previewContent.classList.remove("hidden");

    // با انتخاب فایل، درخواست پیش‌بینی به سرور فرستاده می‌شود.
    sendImageToBackend(file);
}

// ---------------- ارسال تصویر به Flask ----------------
async function sendImageToBackend(file) {
    // نتیجه قبلی را مخفی و حالت بارگذاری را فعال می‌کنیم.
    resultCard.classList.add("hidden");
    tryAgainButton.classList.add("hidden");
    loading.classList.remove("hidden");
    clearError();

    // FormData تصویر را به شکل multipart/form-data ارسال می‌کند.
    const formData = new FormData();
    formData.append("image", file);

    try {
        // آدرس /predict مربوط به تابع پیش‌بینی در app.py است.
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        // پاسخ Flask به صورت JSON خوانده می‌شود.
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "خطا در دریافت پاسخ از سرور.");
        }

        // نتیجه مدل در رابط کاربری قرار می‌گیرد.
        showResult(data, previewUrl);

    } catch (error) {
        showError(error.message || "ارتباط با سرور برقرار نشد.");
    } finally {
        loading.classList.add("hidden");
    }
}

// ---------------- نمایش نتیجه پیش‌بینی ----------------
function showResult(data, imageUrl) {
    const className = data.class_name;
    const confidence = Number(data.confidence);
    const appleProbability = Number(data.probabilities.Apple);
    const orangeProbability = Number(data.probabilities.Orange);

    // نمایش نام کلاس پیش‌بینی‌شده و تصویر آپلودی
    const classEmoji = className === "Apple" ? "🍎" : "🍊";
    const predictedClass = document.getElementById("predictedClass");

    predictedClass.textContent = `${className} ${classEmoji}`;
    predictedClass.classList.toggle("orange-result", className === "Orange");

    resultImage.src = imageUrl;
    document.getElementById("confidenceValue").textContent = `${confidence.toFixed(2)}%`;

    // نمایش درصدهای هر دو کلاس
    document.getElementById("appleProbability").textContent =
        `${appleProbability.toFixed(2)}%`;
    document.getElementById("orangeProbability").textContent =
        `${orangeProbability.toFixed(2)}%`;

    // تنظیم عرض نوارهای احتمال
    document.getElementById("appleBar").style.width =
        `${Math.max(0, Math.min(100, appleProbability))}%`;
    document.getElementById("orangeBar").style.width =
        `${Math.max(0, Math.min(100, orangeProbability))}%`;

    resultCard.classList.remove("hidden");
    tryAgainButton.classList.remove("hidden");
}

// ---------------- نمایش و پاک کردن خطا ----------------
function showError(message) {
    statusMessage.textContent = message;
    statusMessage.classList.remove("hidden");
}

function clearError() {
    statusMessage.textContent = "";
    statusMessage.classList.add("hidden");
}

// ---------------- شروع یک پیش‌بینی جدید ----------------
function resetPage() {
    selectedFile = null;
    imageInput.value = "";

    if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
        previewUrl = null;
    }

    imagePreview.removeAttribute("src");
    resultImage.removeAttribute("src");

    previewContent.classList.add("hidden");
    uploadPrompt.classList.remove("hidden");
    resultCard.classList.add("hidden");
    tryAgainButton.classList.add("hidden");
    loading.classList.add("hidden");
    clearError();
}

tryAgainButton.addEventListener("click", resetPage);

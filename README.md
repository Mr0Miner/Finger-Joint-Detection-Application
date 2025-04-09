# Finger Joint Detection Application

## English

### Overview
This application is designed to detect finger joints in real-time using a webcam, video file, or IP camera. It utilizes the MediaPipe library for hand tracking and OpenCV for image processing. The application provides a graphical user interface (GUI) built with Tkinter, allowing users to interact with the detection process, adjust settings, and save images.

### Features
- **Real-time Detection**: Detects finger joints and counts the number of fingers up.
- **Multiple Input Sources**: Supports webcam, video files, and IP cameras.
- **User-friendly Interface**: Provides a GUI for easy interaction.
- **Image Saving**: Allows users to save the current frame as an image.
- **Hand Tracking**: Tracks up to two hands simultaneously.

### Requirements
- Python 3.x
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- Tkinter (`tkinter`)
- Pillow (`PIL`)

### Installation
1. Clone the repository or download the `main.py` file.
2. Install the required libraries using pip:
   ```bash
   pip install opencv-python mediapipe tkinter pillow
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Usage
1. **Select Input Source**: Choose between webcam, video file, or IP camera.
2. **Start Detection**: Click the "Start" button to begin the detection process.
3. **Stop Detection**: Click the "Stop" button to halt the detection.
4. **Save Image**: Click the "Save Image" button to save the current frame.
5. **Exit**: Click the "Exit" button to close the application.

### Code Structure
- **FingerDetectionApp Class**: Manages the GUI and detection process.
  - `__init__`: Initializes the application and sets up the GUI.
  - `create_widgets`: Creates the GUI components.
  - `start_detection`: Starts the finger joint detection.
  - `stop_detection`: Stops the detection process.
  - `save_image`: Saves the current frame as an image.
  - `detect_finger_joints`: Processes the video feed and detects finger joints.

### Video sample
<details>
   <summary>More Information</summary>
   
   <h3 align="center">Test 1</h3>
   <video width="1280" height="720" controls>
      <source src="https://raw.githubusercontent.com/Mr0Miner/Finger-Joint-Detection-Application/a9ec5518c113cef19a9a1fdad50cd6ce69ec8853/DATA_FOR_TEST/Tested%20Hand%20sample%20video/1_output_video.mp4" type="video/mp4">
      مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.
   </video>

   <hr>

   <h3 align="center">Test 2</h3>
   <video width="1280" height="720" controls>
      <source src="https://raw.githubusercontent.com/Mr0Miner/Finger-Joint-Detection-Application/a9ec5518c113cef19a9a1fdad50cd6ce69ec8853/DATA_FOR_TEST/Tested%20Hand%20sample%20video/2_output_video.mp4" type="video/mp4">
      مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.
   </video>

   <hr>

   <h3 align="center">Test 3</h3>
   <video width="1280" height="720" controls>
      <source src="https://raw.githubusercontent.com/Mr0Miner/Finger-Joint-Detection-Application/a9ec5518c113cef19a9a1fdad50cd6ce69ec8853/DATA_FOR_TEST/Tested%20Hand%20sample%20video/3_output_video.mp4" type="video/mp4">
      مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.
   </video>
</details>

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
## فارسی

### نمای کلی
این برنامه برای تشخیص مفاصل انگشتان در زمان واقعی با استفاده از وب‌کم، فایل ویدیویی یا دوربین IP طراحی شده است. این برنامه از کتابخانه MediaPipe برای ردیابی دست و OpenCV برای پردازش تصویر استفاده می‌کند. برنامه یک رابط کاربری گرافیکی (GUI) با استفاده از Tkinter ارائه می‌دهد که به کاربران امکان تعامل با فرآیند تشخیص، تنظیمات و ذخیره تصاویر را می‌دهد.

### ویژگی‌ها
- **تشخیص در زمان واقعی**: مفاصل انگشتان را تشخیص داده و تعداد انگشتان بالا را می‌شمارد.
- **چندین منبع ورودی**: از وب‌کم، فایل‌های ویدیویی و دوربین‌های IP پشتیبانی می‌کند.
- **رابط کاربری آسان**: یک GUI برای تعامل آسان ارائه می‌دهد.
- **ذخیره تصویر**: به کاربران امکان ذخیره فریم فعلی به عنوان تصویر را می‌دهد.
- **ردیابی دست**: تا دو دست را به طور همزمان ردیابی می‌کند.

### نیازمندی‌ها
- Python 3.13
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- Tkinter (`tkinter`)
- Pillow (`PIL`)

### نصب
1. مخزن را کلون کنید یا فایل `main.py` را دانلود کنید.
2. کتابخانه‌های مورد نیاز را با استفاده از pip نصب کنید:
   ```bash
   pip install opencv-python mediapipe tkinter pillow
   ```
3. برنامه را اجرا کنید:
   ```bash
   python main.py
   ```

### نحوه استفاده
1. **انتخاب منبع ورودی**: بین وب‌کم، فایل ویدیویی یا دوربین IP انتخاب کنید.
2. **شروع تشخیص**: دکمه "Start" را کلیک کنید تا فرآیند تشخیص شروع شود.
3. **توقف تشخیص**: دکمه "Stop" را کلیک کنید تا تشخیص متوقف شود.
4. **ذخیره تصویر**: دکمه "Save Image" را کلیک کنید تا فریم فعلی ذخیره شود.
5. **خروج**: دکمه "Exit" را کلیک کنید تا برنامه بسته شود.

### ساختار کد
- **کلاس FingerDetectionApp**: مدیریت رابط کاربری و فرآیند تشخیص.
  - `__init__`: برنامه را مقداردهی اولیه کرده و GUI را تنظیم می‌کند.
  - `create_widgets`: اجزای GUI را ایجاد می‌کند.
  - `start_detection`: فرآیند تشخیص مفاصل انگشتان را شروع می‌کند.
  - `stop_detection`: فرآیند تشخیص را متوقف می‌کند.
  - `save_image`: فریم فعلی را به عنوان تصویر ذخیره می‌کند.
  - `detect_finger_joints`: ویدیو را پردازش کرده و مفاصل انگشتان را تشخیص می‌دهد.

### نمونه ویدیویی
<details>
   <summary>اطلاعات بیشتر</summary>
   
   <h3 align="center">تست 1</h3>
   <video width="1280" height="720" controls>
      <source src="DATA_FOR_TEST/Tested Hand sample video/1_output_video.mp4" type="video/mp4">
      مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.
   </video>

   <hr>

   <h3 align="center">تست 2</h3>
   <video width="1280" height="720" controls>
      <source src="DATA_FOR_TEST/Tested Hand sample video/2_output_video.mp4" type="video/mp4">
      مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.
   </video>

   <hr>

   <h3 align="center">تست 3</h3>
   <video width="1280" height="720" controls>
      <source src="DATA_FOR_TEST/Tested Hand sample video/3_output_video.mp4" type="video/mp4">
      مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.
   </video>
</details>

### مشارکت
مشارکت‌ها مورد استقبال هستند! لطفاً مخزن را فورک کرده و یک درخواست pull با تغییرات خود ارسال کنید.

### مجوز
این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر به فایل [LICENSE](LICENSE) مراجعه کنید.

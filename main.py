import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import threading

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class FingerDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finger Joint Detection")
        
        self.camera_source = 0
        self.min_detection_confidence = 0.5
        self.max_num_hands = 2
        
        self.create_widgets()
        
        self.cap = None
        self.is_running = False

    def create_widgets(self):
        self._create_image_frame()
        self._create_settings_frame() 
        self._create_info_frame()
        self._create_save_frame()

    def _create_image_frame(self):
        self.image_frame = ttk.LabelFrame(self.root, text="Live Feed")
        self.image_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _create_settings_frame(self):
        self.settings_frame = ttk.LabelFrame(self.root, text="Settings")
        self.settings_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self._create_input_frame()
        self._create_control_frame()
        self._create_action_frame()

    def _create_input_frame(self):
        self.input_frame = ttk.Frame(self.settings_frame)
        self.input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(self.input_frame, text="Input Source:").grid(row=0, column=0, padx=5, pady=5)
        
        self.source_var = tk.StringVar(value="camera")
        # self.source_var.trace('w', self.on_source_change)
        
        ttk.Radiobutton(self.input_frame, text="Webcam", variable=self.source_var, value="camera").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.input_frame, text="Video File", variable=self.source_var, value="video").grid(row=0, column=2, padx=5)
        ttk.Radiobutton(self.input_frame, text="IP Camera", variable=self.source_var, value="ip").grid(row=0, column=3, padx=5, pady=5)
        
        self.camera_var = tk.IntVar(value=0)
        self.camera_button = ttk.Button(self.input_frame, text="Switch Camera", command=self.switch_camera)

    def _create_control_frame(self):
        ttk.Separator(self.settings_frame, orient="vertical").grid(row=0, column=1, sticky="ns", padx=5)
        
        self.control_frame = ttk.Frame(self.settings_frame)
        self.control_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_detection)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

    def _create_action_frame(self):
        ttk.Separator(self.settings_frame, orient="vertical").grid(row=0, column=3, sticky="ns", padx=5)
        
        self.action_frame = ttk.Frame(self.settings_frame)
        self.action_frame.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")
        
        ttk.Button(self.action_frame, text="Settings", command=self.open_settings).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.action_frame, text="Exit", command=self.root.destroy).grid(row=0, column=1, padx=5, pady=5)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("تنظیمات")
        settings_window.geometry("300x200")
        
        # Switch Camera button in settings window
        ttk.Button(settings_window, text="Switch Camera", command=self.switch_camera).pack(padx=20, pady=20)

    def _create_info_frame(self):
        self.Information_frame = ttk.LabelFrame(self.root, text="Information")
        self.Information_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.fingers_label = ttk.Label(self.Information_frame, text="Fingers Up: 0")
        self.fingers_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        self.hand_count_label = ttk.Label(self.Information_frame, text="Detected Hands: 0")
        self.hand_count_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def _create_save_frame(self):
        self.save_frame = ttk.LabelFrame(self.root, text="Save")
        self.save_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#    def on_source_change(self, *args):
#        if self.source_var.get() == "camera":
#            self.camera_button.grid()
#        else:
#           self.camera_button.grid_remove()

    def switch_camera(self):
        if self.source_var.get() == "camera":
            self.camera_var.set((self.camera_var.get() + 1) % 2)
            if self.is_running:
                self.stop_detection()
                self.start_detection()

    def start_detection(self):
        source = self.source_var.get()
        if not self._setup_video_source(source):
            return
            
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Input source not accessible!")
            return
        
        self._update_button_states(True)
        self.is_running = True
        
        self.thread = threading.Thread(target=self.detect_finger_joints)
        self.thread.daemon = True
        self.thread.start()

    def _setup_video_source(self, source):
        if source == "camera":
            self.cap = cv2.VideoCapture(self.camera_var.get())
        elif source == "video":
            file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
            if not file_path:
                return False
            self.cap = cv2.VideoCapture(file_path)
        elif source == "ip":
            ip_address = simpledialog.askstring("IP Address", "Enter camera IP address: \nExample: 192.168.1.100:4747")
            if not ip_address:
                return False
            self.cap = cv2.VideoCapture(f"http://{ip_address}/video")
        return True

    def _update_button_states(self, is_running):
        self.start_button.config(state=tk.DISABLED if is_running else tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL if is_running else tk.DISABLED)

    def stop_detection(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self._update_button_states(False)
        self.canvas.delete("all")

    def detect_finger_joints(self):
        try:
            with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=self.max_num_hands,
                min_detection_confidence=self.min_detection_confidence) as hands:
                
                while self.is_running and self.cap.isOpened():
                    success, image = self.cap.read()
                    if not success:
                        continue
                    
                    image = self._process_image(image, hands)
                    
                    if cv2.waitKey(5) & 0xFF == ord('q'):
                        break
            
            self._cleanup()
            
        except Exception as e:
            print(f"Error in detect_finger_joints: {e}")
            self.stop_detection()

    def _process_image(self, image, hands):
        h, w = image.shape[:2]
        if w > 800 or h > 600:
            image = cv2.resize(image, (800, 600))
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        
        total_fingers_up = 0
        hand_count = 0
        
        if results.multi_hand_landmarks:
            hand_count = len(results.multi_hand_landmarks)
            self.root.after(0, lambda: self.hand_count_label.config(text=f"Detected Hands: {hand_count}"))
            
            for hand_landmarks in results.multi_hand_landmarks:
                total_fingers_up += self._process_hand_landmarks(image, hand_landmarks)
        
        self._update_display(image, total_fingers_up)
        return image

    def _process_hand_landmarks(self, image, hand_landmarks):
        h, w, _ = image.shape
        joints = self._get_joint_positions(image, hand_landmarks)
        self._draw_hand_connections(image, joints)
        return self._count_fingers_up(joints)

    def _get_joint_positions(self, image, hand_landmarks):
        h, w, _ = image.shape
        joints = []
        for idx in range(21):
            lm = hand_landmarks.landmark[idx]
            cx = int(lm.x * w)
            cy = int(lm.y * h)
            joints.append((cx, cy))
            cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
        return joints

    def _draw_hand_connections(self, image, joints):
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (5, 6), (6, 7), (7, 8),
            (9, 10), (10, 11), (11, 12),
            (13, 14), (14, 15), (15, 16),
            (17, 18), (18, 19), (19, 20),
            (5, 0), (9, 0), (13, 0), (17, 0)
        ]
        for start, end in connections:
            cv2.line(image, joints[start], joints[end], (0, 255, 0), 2)

    def _count_fingers_up(self, joints):
        fingers_up = [False] * 5
        tip_indices = [4, 8, 12, 16, 20]
        for i, tip_index in enumerate(tip_indices):
            if tip_index == 4:  # Thumb
                fingers_up[i] = joints[tip_index][0] < joints[tip_index-1][0]
            else:  # Other fingers
                fingers_up[i] = joints[tip_index][1] < joints[tip_index-2][1]
        return sum(fingers_up)

    def _update_display(self, image, total_fingers_up):
        self.current_image = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        self.root.after(0, lambda: self.update_canvas(photo))
        self.root.after(0, lambda: self.fingers_label.config(text=f"Fingers Up: {total_fingers_up}"))

    def _cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def update_canvas(self, photo):
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = FingerDetectionApp(root)
    root.mainloop()
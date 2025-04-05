import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import cv2
import mediapipe as mp

class FingerJointDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finger Joint Detection")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.is_processing = False
        
        # Styling
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Main Frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input File Selection
        ttk.Label(self.main_frame, text="Input Video:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.input_entry = ttk.Entry(self.main_frame, textvariable=self.input_path, width=40)
        self.input_entry.grid(row=1, column=0, padx=(0, 5))
        ttk.Button(self.main_frame, text="Browse", command=self.browse_input).grid(row=1, column=1)
        
        # Output File Selection
        ttk.Label(self.main_frame, text="Output Video:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        self.output_entry = ttk.Entry(self.main_frame, textvariable=self.output_path, width=40)
        self.output_entry.grid(row=3, column=0, padx=(0, 5))
        ttk.Button(self.main_frame, text="Browse", command=self.browse_output).grid(row=3, column=1)
        
        # Progress Bar
        self.progress_label = ttk.Label(self.main_frame, text="Ready")
        self.progress_label.grid(row=4, column=0, columnspan=2, pady=(20, 5))
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=(0, 20))
        
        # Action Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=6, column=0, columnspan=2)
        
        self.process_btn = ttk.Button(self.button_frame, text="Start Processing", command=self.start_processing)
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(self.button_frame, text="Cancel", command=self.cancel_processing, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Set default output path
        self.output_path.set("output_video.mp4")
    
    def browse_input(self):
        filepath = filedialog.askopenfilename(
            title="Select Input Video",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("All Files", "*.*")]
        )
        if filepath:
            self.input_path.set(filepath)
            # Set default output path based on input
            if not self.output_path.get():
                import os
                dirname, filename = os.path.split(filepath)
                name, ext = os.path.splitext(filename)
                self.output_path.set(os.path.join(dirname, f"{name}_output{ext}"))
    
    def browse_output(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Output Video",
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4"), ("AVI Files", "*.avi"), ("All Files", "*.*")]
        )
        if filepath:
            self.output_path.set(filepath)
    
    def start_processing(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input video file")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please specify an output file path")
            return
        
        self.is_processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_label.config(text="Processing...")
        
        # Run processing in a separate thread
        processing_thread = threading.Thread(
            target=self.run_detection,
            args=(self.input_path.get(), self.output_path.get()),
            daemon=True
        )
        processing_thread.start()
        
        # Check progress periodically
        self.check_progress()
    
    def run_detection(self, input_path, output_path):
        try:
            self.progress.set(0)
            detect_finger_joints(input_path, output_path)
            self.progress.set(100)
            if self.is_processing:  # Only show success if not cancelled
                messagebox.showinfo("Success", "Processing completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.is_processing = False
            self.root.after(0, self.reset_ui)
    
    def check_progress(self):
        if self.is_processing:
            current = self.progress.get()
            if current < 90:  # Simulate progress (you can replace with actual progress tracking)
                self.progress.set(current + 10)
            self.root.after(500, self.check_progress)
    
    def cancel_processing(self):
        self.is_processing = False
        self.progress_label.config(text="Cancelling...")
        # Note: Actual cancellation would need more complex implementation
        self.reset_ui()
        messagebox.showinfo("Cancelled", "Processing was cancelled")
    
    def reset_ui(self):
        self.process_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Ready")
        if not self.is_processing:
            self.progress.set(0)

# Your existing detection function
def detect_finger_joints(input_video_path, output_video_path):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break
            
            if out is None:
                h, w = image.shape[:2]
                out = cv2.VideoWriter(output_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))
            
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    h, w, c = image.shape
                    joints = []
                    
                    indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
                    
                    for idx in indices:
                        lm = hand_landmarks.landmark[idx]
                        cx = int(lm.x * w)
                        cy = int(lm.y * h)
                        joints.append((cx, cy))
                        cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
                    
                    # اتصال نقاط مفاصل
                    cv2.line(image, joints[0], joints[1], (0, 255, 0), 2)
                    cv2.line(image, joints[1], joints[2], (0, 255, 0), 2) 
                    cv2.line(image, joints[2], joints[3], (0, 255, 0), 2)
                    cv2.line(image, joints[3], joints[4], (0, 255, 0), 2)

                    cv2.line(image, joints[5], joints[6], (0, 255, 0), 2)
                    cv2.line(image, joints[6], joints[7], (0, 255, 0), 2)
                    cv2.line(image, joints[7], joints[8], (0, 255, 0), 2)

                    cv2.line(image, joints[9], joints[10], (0, 255, 0), 2)
                    cv2.line(image, joints[10], joints[11], (0, 255, 0), 2)
                    cv2.line(image, joints[11], joints[12], (0, 255, 0), 2)

                    cv2.line(image, joints[13], joints[14], (0, 255, 0), 2)
                    cv2.line(image, joints[14], joints[15], (0, 255, 0), 2)
                    cv2.line(image, joints[15], joints[16], (0, 255, 0), 2)

                    cv2.line(image, joints[17], joints[18], (0, 255, 0), 2)
                    cv2.line(image, joints[18], joints[19], (0, 255, 0), 2)
                    cv2.line(image, joints[19], joints[20], (0, 255, 0), 2)
                    
                    base_indices = [17, 13, 9, 5]
                    for idx in base_indices:
                        cv2.line(image, joints[0], joints[idx], (0, 255, 0), 2)
                    
            out.write(image)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = FingerJointDetectorApp(root)
    root.mainloop()
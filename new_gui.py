import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk
import threading 
import os
import cv2

def open_full_image(image_path):
    # Create a new thread for displaying the image
    thread = threading.Thread(target=show_full_image, args=(image_path,))
    thread.start()  

# Function to display the full image when clicked
def show_full_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not open or find the image.")
        return
    org_image = image.copy()
    max_zoom_level = 5.0
    zoom_level = 1.0

    def zoom(event, x, y, flags, param):
        nonlocal zoom_level, image
        if event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                zoom_level = min(max_zoom_level, zoom_level + 0.1)
            else:
                zoom_level = max(0.1, zoom_level - 0.1)

            new_size = (int(org_image.shape[1] * zoom_level), int(org_image.shape[0] * zoom_level))
            image = cv2.resize(org_image, new_size)

    cv2.namedWindow('Zoomable Image')
    cv2.setMouseCallback('Zoomable Image', zoom)
    while True:
        cv2.imshow('Zoomable Image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

# Function to clear the thumbnail frame
def clear_thumbnails():
    for widget in thumbnail_frame.winfo_children():
        widget.destroy()

# Function to handle folder selection for Image Directory 1
def select_folder():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        images_folder_entry.delete(0, tk.END)
        images_folder_entry.insert(0, selected_dir)
    

# Function to handle folder selection for Im
# Function to handle viewing thumbnails
def start_detection():
    image_dir1 = images_folder_entry.get()  # Get the directory from the Entry widget
    
    # Check if the directory is valid and not empty
    if not image_dir1 or not os.path.exists(image_dir1):
        messagebox.showerror("Error", "Please select a valid directory!")
        return

    image_files1 = [f for f in os.listdir(image_dir1) if f.endswith(".png") or f.endswith(".jpg")]
    if len(image_files1) == 0:
        messagebox.showerror("Error", "No images found in the selected directory!")
        return
    clear_thumbnails()

    total_images = len(image_files1)
    if total_images == 0:
        messagebox.showerror("Error", "No images found in the directories!")
        return
    
    progress_var.set(0)
    num_columns = 19
    row_frame = tk.Frame(thumbnail_frame)
    row_frame.pack(anchor='nw')
    thumbnail_image = Image.open("image12.png")

    # Add images from directory 1 with green border
    for idx, image_file in enumerate(image_files1):
        image_path = os.path.join(image_dir1, image_file)
        thumbnail_path = "images.png"
        #thumbnail_path = create_thumbnail_with_border(event_count, image_path, border_color="red")

        if thumbnail_path:
            thumbnail_image = Image.open(thumbnail_path)
            thumbnail_image = ImageTk.PhotoImage(thumbnail_image)
            thumb_button = tk.Button(row_frame, image=thumbnail_image, bg="#003333", width=50, height =50, borderwidth=5,  relief="sunken", highlightbackground="#005555", highlightcolor="#000555" , command=lambda p=image_path: open_full_image(p))
            thumb_button.image = thumbnail_image
            thumb_button.grid(row=idx // num_columns, column=idx % num_columns)
        thumbnail_frame.update_idletasks()

        progress_var.set((len(image_files1) + idx + 1) / total_images * 100)

# Setup tkinter window
root = tk.Tk()
#root.title("")
root.geometry("1280x720")
root.configure(bg='#001010')

# Variables
image_dir1 = ""
image_files1 = []
event_count = 0
progress_var = tk.DoubleVar()
bg='#002222'
global images_folder_entry

# Create Frames and Layouts
# Heading
heading_frame = tk.Frame(root, bg='#124E66', padx=20, pady=10)
heading_frame.pack(fill=tk.X)
heading_label = tk.Label(heading_frame, text="OBJECT DETECTION", font=("Helvetica", 18, "bold"), fg="#ffffff", bg="#124E66")
heading_label.pack()

# Horizontal Separator
tk.Frame(root, height=2, bd=2, relief=tk.SUNKEN).pack(fill=tk.X, padx=10, pady=20)

# Controls Frame
controls_frame = tk.Frame(root, bg=bg,relief="groove", name="controls_frame",width=380, height=650)
controls_frame.pack(side=tk.LEFT,fill=tk.BOTH, padx=10)
controls_frame.pack_propagate=(False)

result = tk.Frame(controls_frame,bg=bg)
result.pack(side=tk.TOP)
input_var = tk.StringVar()
tk.Label(result, text="CONTROLS", font=("Helvetica", 10, "bold"), fg="#ffffff",width=48, bg="#001111").pack(anchor='w')

#directory 
images_folder_dir = "images2/"
input1 = tk.Frame(controls_frame, bg=bg)
input1.pack(side=tk.TOP, anchor='w')
tk.Label(input1, text="Image Dir", font=("Helvetica", 10, "bold"), fg="#ffffff", width=15, bg=bg).pack(side=tk.LEFT, pady=5, anchor='w')
images_folder_entry = tk.Entry(input1, width=30, bg="#fff9c4")
images_folder_entry.pack(side=tk.LEFT, padx=5)
images_folder_entry.insert(0, images_folder_dir) 
tk.Button(input1, text="Browse", command=select_folder, bg="#124E56", fg="#FFFFFF").pack(side=tk.LEFT, padx=5, anchor='w')


#output dir
input2 = tk.Frame(controls_frame,bg=bg)
input2.pack(side=tk.TOP, anchor='w')
tk.Label(input2, text="Output Dir", font=("Helvetica", 10, "bold"), fg="#ffffff",width=15, bg=bg).pack(side=tk.LEFT,anchor='w', pady=2)
Output = tk.Entry(input2, width=30, bg="#748D92", fg="#ffffff")
Output.pack(side=tk.LEFT,anchor='w', padx=5, pady=2)
tk.Button(input2, text="Browse", bg="#124E56", fg="#FFFFFF").pack(side=tk.LEFT,anchor='w', padx=5, pady=2)

#model input
input3 = tk.Frame(controls_frame,bg=bg)
input3.pack(side=tk.TOP, anchor='w')
tk.Label(input3, text="Model", font=("Helvetica", 10, "bold"), fg="#ffffff",width=15, bg=bg).pack(side=tk.LEFT,anchor='w', pady=2)
Model = tk.Entry(input3, width=30, bg="#748D92", fg="#000000")
Model.pack(side=tk.LEFT,anchor='w', padx=5, pady=2)
tk.Button(input3, text="Browse", bg="#124E56", fg="#FFFFFF").pack(side=tk.LEFT,anchor='w', padx=5,pady=2)

#image size
input5 = tk.Frame(controls_frame,bg=bg)
input5.pack(side=tk.TOP,  anchor='w')
tk.Label(input5, text="Image Size", font=("Helvetica", 10, "bold"), fg="#ffffff",width=15, bg=bg, pady=2).pack(side=tk.LEFT,pady=2,  anchor='w')
Size = tk.Entry(input5, width=30, bg="#748D92", fg="#000000")
Size.pack(side=tk.LEFT, padx=5,  anchor='w')

#threshold
input5 = tk.Frame(controls_frame,bg=bg)
input5.pack(side=tk.TOP,  anchor='w')
tk.Label(input5, text="Threshold", font=("Helvetica", 10, "bold"), fg="#ffffff",width=15, bg=bg, pady=2).pack(side=tk.LEFT,pady=2,  anchor='w')
Threshold = tk.Entry(input5, width=30, bg="#748D92", fg="#000000")
Threshold.pack(side=tk.LEFT, padx=5,  anchor='w')


#iou threshold
input6 = tk.Frame(controls_frame,bg=bg)
input6.pack(side=tk.TOP,  anchor='w')
tk.Label(input6, text="IOU Threshold", font=("Helvetica", 10, "bold"), fg="#ffffff",width=15, bg=bg, pady=2).pack(side=tk.LEFT,pady=2,  anchor='w')
IOU = tk.Entry(input6, width=30, bg="#748D92", fg="#000000")
IOU.pack(side=tk.LEFT, padx=5,  anchor='w')


#classes
classes = ["Class A", "Class B", "Class C"]  # Example classes
input7 = tk.Frame(controls_frame, bg=bg)
input7.pack(side=tk.TOP, anchor='w')
tk.Label(input7, text="Class", font=("Helvetica", 10, "bold"), fg="#ffffff", width=15, bg=bg).pack(side=tk.LEFT, pady=2)
class_dropdown = ttk.Combobox(input7, values=classes, width=27)
class_dropdown.set(classes[0])  # Set default value (first class)
class_dropdown.pack(side=tk.LEFT, padx=5)


#Progress Bar
progress_bar = ttk.Progressbar(controls_frame, variable=progress_var, maximum=100, length=380)
progress_bar.pack(side=tk.TOP,anchor='w', padx=5, pady=15)


#buttons
Button = tk.Frame(controls_frame,bg=bg)
Button.pack(side=tk.TOP,pady=5)
tk.Button(Button, text="Start Detection", command=start_detection,width=11, bg="#006699", fg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(side=tk.LEFT,anchor='w', padx=5, pady=5)
tk.Button(Button, text="Save Images", command="",width=11, bg="#006699", fg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(side=tk.LEFT,anchor='w', padx=5, pady=5)
tk.Button(Button, text="Clear", command=clear_thumbnails,width=11, bg="#006699", fg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(side=tk.LEFT,anchor='w', padx=5, pady=5)
tk.Button(Button, text="Exit", command=root.destroy,width=11, bg="#006699", fg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(side=tk.LEFT,anchor='w', padx=5, pady=5)

#Result widgets
result = tk.Frame(controls_frame,bg=bg)
result.pack(side=tk.TOP)
input_var = tk.StringVar()
tk.Label(result, text="R E S U L T", font=("Helvetica", 10, "bold"), fg="#ffffff",width=48, bg="#001111").pack(anchor='w', pady=5)

result1 = tk.Frame(controls_frame,bg=bg)
result1.pack(side=tk.TOP, anchor='w')
input_var = tk.StringVar()
tk.Label(result1, text="Result 1", font=("Helvetica", 10, "bold"), fg="#ffffff", width=15, bg=bg).pack(side=tk.LEFT,anchor='w', padx=5, pady=5)
result1_entry = tk.Text(result1, width=20, bg="#748D92", height=1, fg="#000000")
result1_entry.pack(anchor='w', padx=5, pady=5,side=tk.LEFT)
result1_entry.config(state="disabled")

result2 = tk.Frame(controls_frame,bg=bg)
result2.pack(side=tk.TOP, anchor='w')
input_var = tk.StringVar()
tk.Label(result2, text="Result 2", font=("Helvetica", 10, "bold"), fg="#ffffff", width=15, bg=bg).pack(side=tk.LEFT,anchor='w', padx=5, pady=5)
result2_entry = tk.Text(result2, width=20,height=1, bg="#748D92", fg="#000000")
result2_entry.pack(anchor='w', padx=5, pady=5,side=tk.LEFT)
result2_entry.config(state="disabled")


result3 = tk.Frame(controls_frame,bg=bg)
result3.pack(side=tk.TOP, anchor='w')
input_var = tk.StringVar()
tk.Label(result3, text="Result 3", font=("Helvetica", 10, "bold"), fg="#ffffff", width=15, bg=bg).pack(side=tk.LEFT,anchor='w', padx=5, pady=5)
result3_entry = tk.Text(result3, width=20,height=1, bg="#748D92", fg="#000000")
result3_entry.pack(anchor='w', padx=5, pady=5,side=tk.LEFT)
result3_entry.config(state="disabled")




# Thumbnails Frame
result = tk.Frame(root,bg=bg)
result.pack(side=tk.TOP)
input_var = tk.StringVar()
tk.Label(result, text="DETECTIONS", font=("Helvetica", 10, "bold"), fg="#ffffff",width=120, bg="#001111").pack(fill=tk.X,anchor='w')

canvas = tk.Canvas(root, bg=bg,highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

thumbnail_frame = tk.Frame(canvas, bg=bg, height=500)
thumbnail_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=thumbnail_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.configure(scrollregion=canvas.bbox("all"))

#thumbnail_frame = tk.Frame(root, bg='#003333', width=1000, height=600, bd = 5 )
#thumbnail_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)

# Main loop
root.mainloop()

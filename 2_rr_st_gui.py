import streamlit as st
import threading
import os
import time

# ---------------------- Thread Function (NO Streamlit calls) ----------------------
def inference_thread(image_files, stop_event, shared_state):
    total = len(image_files)

    for i in range(total):
        if stop_event.is_set():
            shared_state["status"] = "stopped"
            return

        time.sleep(0.2)  # simulate processing
        shared_state["progress"] = int(((i + 1) / total) * 100)
        shared_state["message"] = f"Processing {i + 1}/{total}"

    shared_state["status"] = "completed"


# ---------------------- Session State Init ----------------------
if "thread_running" not in st.session_state:
    st.session_state.thread_running = False
    st.session_state.stop_event = threading.Event()
    st.session_state.shared_state = {
        "progress": 0,
        "status": None,
        "message": "Execution status"
    }


# ---------------------- Sidebar (Controls) ----------------------
st.sidebar.title("Controls")

image_dir1 = st.sidebar.text_input("Image Directory1", "img4/")
image_dir2 = st.sidebar.text_input("Image Directory2", "img3/")
model_path = st.sidebar.text_input("Model Path")
output_dir = st.sidebar.text_input("Output Directory")
conf_thresh = st.sidebar.text_input("Conf-Threshold", "0.25")
img_size = st.sidebar.text_input("Image Size", "640")

start_btn = st.sidebar.button(
    "Start Detection",
    disabled=st.session_state.thread_running
)

stop_btn = st.sidebar.button(
    "Stop",
    disabled=not st.session_state.thread_running
)

exit_btn = st.sidebar.button("Exit")


# ---------------------- Exit ----------------------
if exit_btn:
    st.stop()


# ---------------------- Start Detection ----------------------
if start_btn:
    if not os.path.isdir(image_dir1):
        st.session_state.shared_state["message"] = "Invalid image directory"

    else:
        image_files = [
            f for f in os.listdir(image_dir1)
            if f.lower().endswith((".jpg", ".png"))
        ]

        if not image_files:
            st.session_state.shared_state["message"] = "No images found"

        else:
            st.session_state.thread_running = True
            st.session_state.stop_event.clear()

            st.session_state.shared_state = {
                "progress": 0,
                "status": None,
                "message": "Detection started"
            }

            threading.Thread(
                target=inference_thread,
                args=(
                    image_files,
                    st.session_state.stop_event,
                    st.session_state.shared_state
                ),
                daemon=True
            ).start()


# ---------------------- Stop Detection ----------------------
if stop_btn:
    st.session_state.stop_event.set()
    st.session_state.shared_state["message"] = "Stopping detection..."


# ---------------------- Main UI ----------------------
st.title("OBJECT DETECTION")

st.progress(st.session_state.shared_state["progress"])
st.info(st.session_state.shared_state["message"])


# ---------------------- Task Completion Handling ----------------------
status = st.session_state.shared_state["status"]

if status == "completed":
    st.success("Detection complete")
    st.session_state.thread_running = False

elif status == "stopped":
    st.warning("Detection stopped")
    st.session_state.thread_running = False


# ---------------------- Thumbnails Placeholder ----------------------
st.subheader("Images")
st.write("Thumbnail panel (same role as right panel in PySimpleGUI)")

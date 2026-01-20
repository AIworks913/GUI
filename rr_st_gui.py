import streamlit as st

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Update Detection Tool",
    layout="wide"
)

# ---------------- Session State ----------------
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

/* Header */
.header {
    background: linear-gradient(90deg, #1e293b, #334155);
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Card */
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}

/* Progress bar fake */
.progress-bg {
    background-color: #334155;
    height: 18px;
    border-radius: 10px;
}
.progress-fill {
    background-color: #22c55e;
    height: 18px;
    width: 75%;
    border-radius: 10px;
}

/* Sidebar */
.sidebar-box {
    background-color: #e5e7eb;
    padding: 15px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Layout ----------------
left, center = st.columns([0.1, 4])

# ================= LEFT SIDEBAR =================
with left:
    st.sidebar.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.sidebar.markdown("### Sub-Control")
    st.sidebar.button("Option 1", use_container_width=True)
    st.sidebar.button("Option 2", use_container_width=True)
    st.sidebar.button("Option 3", use_container_width=True)
    st.sidebar.button("Option 4", use_container_width=True)
    st.sidebar.button("Option 5", use_container_width=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ================= CENTER =================
with center:

    # Header
    st.markdown('<div class="header">Update Detection Tool</div>', unsafe_allow_html=True)

    # Progress
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Progress: 75%")
    st.markdown("""
    <div class="progress-bg">
        <div class="progress-fill"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Buttons
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("Check Updates")
    c2.button("Start Scan")
    c3.button("Download Update")
    c4.button("Settings")
    c5.button("View Logs")

    c6, c7 = st.columns(5)[:2]
    c6.button("Pause")
    c7.button("Exit")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Thumbnails ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Generated Thumbnails")

    images = [
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
        "https://images.unsplash.com/photo-1491553895911-0055eca6402d",
        "https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
        "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
        "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13",
        "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
        "https://images.unsplash.com/photo-1520975916090-3105956dac38",
        "https://images.unsplash.com/photo-1519681393784-d120267933ba"
    ]

    cols = st.columns(4)

    for idx, img in enumerate(images):
        with cols[idx % 4]:

            st.markdown(f"""
            <div id="thumb-{idx}">
            """, unsafe_allow_html=True)

            clicked = st.button("", key=f"thumb_btn_{idx}")

            st.markdown(f"""
            <style>
            #thumb-{idx} button {{
                background-image: url("{img}");
                background-size: cover;
                background-position: center;
                width: 100%;
                height: 160px;
                border-radius: 8px;
                border: none;
                padding: 0;
            }}
            </style>
            </div>
            """, unsafe_allow_html=True)

            if clicked:
                st.session_state.selected_image = img

    # ---------------- Full Image Viewer ----------------
    if st.session_state.selected_image:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Full Image View")
        st.image(st.session_state.selected_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

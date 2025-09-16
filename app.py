import streamlit as st
from waveform_player import waveform_player
import re

# --- Helper Functions ---
def is_valid_timestamp_format(timestamp):
    """Check if timestamp is in mm:ss or mm:ss.fff format"""
    pattern = r'^\d{1,2}:\d{2}(\.\d{1,3})?$'
    return re.match(pattern, timestamp) is not None

# --- App Config ---
st.set_page_config(
    page_title="Synced Lyrics Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Title and Description ---
st.title("🎵 Synced Lyrics Generator")
st.markdown("""
Upload an audio file and a .txt lyrics file.
Use the waveform player to find the correct time for each lyric line, then click "Set".
""")

# --- Session State Initialization ---
if "lyrics" not in st.session_state:
    st.session_state.lyrics = []
if "sync_times" not in st.session_state:
    st.session_state.sync_times = []
if "lyrics_file_name" not in st.session_state:
    st.session_state.lyrics_file_name = None

# --- 1. Audio Upload Section ---
st.header("1. Upload Audio File")
audio_file = st.file_uploader(
    "Choose an audio file (mp3, wav, etc.)",
    type=["mp3", "wav", "ogg", "flac"],
)

# --- 2. Upload Lyrics File Section ---
st.header("2. Upload Lyrics File")
lyrics_file = st.file_uploader(
    "Upload a .txt file with your lyrics (one line per lyric):",
    type=["txt"],
)

# Repopulate lyrics if a new file is uploaded
if lyrics_file and (st.session_state.lyrics_file_name != lyrics_file.name):
    st.session_state.lyrics_file_name = lyrics_file.name
    lyrics_content = lyrics_file.read().decode("utf-8")
    st.session_state.lyrics = [line.strip() for line in lyrics_content.splitlines() if line.strip()]
    st.session_state.sync_times = [""] * len(st.session_state.lyrics)
    # Clear old widget states to prevent conflicts
    for i in range(len(st.session_state.lyrics) + 20): # Clear a few extra keys just in case
        st.session_state.pop(f"lyric_{i}", None)
        st.session_state.pop(f"timestamp_{i}", None)
        st.session_state.pop(f"set_{i}", None)
    st.rerun()


# --- 3. Audio Visualization Section ---
st.header("3. Audio Visualization")
if audio_file:
    audio_bytes = audio_file.read()
    waveform_player(
        audio_bytes=audio_bytes,
        key="waveform_player",
        height=120,
        show_controls=True,
    )
else:
    st.info("Waveform will appear here after audio upload.")


# --- 4. Sync Lyrics Section ---
st.header("4. Sync Lyrics")
if audio_file and st.session_state.lyrics:
    st.write("Edit lyrics and click 'Set' to capture the current timestamp.")

    col1, col2, col3 = st.columns([4, 2, 1])
    col1.write("**Lyric Text**")
    col2.write("**Timestamp (mm:ss.ms)**")
    col3.write("**Sync**")

    for i, lyric in enumerate(st.session_state.lyrics):
        c1, c2, c3 = st.columns([4, 2, 1])
        with c1:
            st.text_input("Lyric", value=st.session_state.lyrics[i], key=f"lyric_{i}", label_visibility="collapsed")
        with c2:
            st.text_input("Timestamp", value=st.session_state.sync_times[i], key=f"timestamp_{i}", label_visibility="collapsed")
        with c3:
            if st.button("Set", key=f"set_{i}"):
                # Persist all current text edits from the widgets' state into the canonical lists.
                for j in range(len(st.session_state.lyrics)):
                    if f"lyric_{j}" in st.session_state:
                        st.session_state.lyrics[j] = st.session_state[f"lyric_{j}"]
                    if f"timestamp_{j}" in st.session_state:
                        st.session_state.sync_times[j] = st.session_state[f"timestamp_{j}"]

                # Apply the 'Set' action for the current line.
                current_time = st.session_state.get("waveform_player", 0.0)
                minutes = int(current_time // 60)
                seconds = int(current_time % 60)
                milliseconds = int((current_time % 1) * 1000)
                st.session_state.sync_times[i] = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                st.rerun()
else:
    st.info("Upload audio and lyrics to begin syncing.")

# --- 5. Export Synced Lyrics Section ---
st.header("5. Export Synced Lyrics")
if st.session_state.lyrics and any(t for t in st.session_state.sync_times):
    # Placeholder for export functionality
    st.success("Export functionality coming soon: Download your synced lyrics as an LRC file.")
else:
    st.info("Sync at least one lyric line to enable export.")

# --- Sidebar: About/Help ---
with st.sidebar:
    st.markdown("## About")
    st.markdown("""
    This app helps you manually sync lyrics to music for karaoke or lyric videos.
    - Built with [Streamlit](https://streamlit.io/)
    """)
    st.markdown("**MVP Version** – core features only.")
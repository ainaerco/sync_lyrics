import os
import re

import streamlit as st
from waveform_player import waveform_player


# --- Helper Functions ---
def is_valid_timestamp_format(timestamp):
    """Check if timestamp is in mm:ss or mm:ss.fff format"""
    if not isinstance(timestamp, str):
        return False
    pattern = r"^\d{1,2}:\d{2}(\.\d{1,3})?$"  # Corrected regex pattern
    return re.match(pattern, timestamp) is not None


def persist_editor_state():
    """Save the current values from the text input widgets into the canonical session state lists."""
    if "lyrics" in st.session_state and st.session_state.lyrics:
        for i in range(len(st.session_state.lyrics)):
            if f"lyric_{i}" in st.session_state:
                st.session_state.lyrics[i] = st.session_state[f"lyric_{i}"]
            if f"timestamp_{i}" in st.session_state:
                st.session_state.sync_times[i] = st.session_state[f"timestamp_{i}"]


def clear_editor_widget_state(num_lines):
    """Clear session state for all lyric editor widgets to prevent stale data."""
    for i in range(num_lines):
        st.session_state.pop(f"lyric_{i}", None)
        st.session_state.pop(f"timestamp_{i}", None)
        st.session_state.pop(f"set_{i}", None)
        st.session_state.pop(f"delete_{i}", None)


# --- App Config ---
st.set_page_config(
    page_title="Synced Lyrics Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Title and Description ---
st.title("🎵 Synced Lyrics Generator")
st.markdown("""
Upload an audio file to start. You can add lyrics manually or upload a .txt file.
""")

# --- Session State Initialization ---
if "lyrics" not in st.session_state:
    st.session_state.lyrics = []
if "sync_times" not in st.session_state:
    st.session_state.sync_times = []
if "lyrics_file_name" not in st.session_state:
    st.session_state.lyrics_file_name = None
if "audio_file_name" not in st.session_state:
    st.session_state.audio_file_name = None
if "num_lyrics_lines" not in st.session_state:
    st.session_state.num_lyrics_lines = 0

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

# --- State Reset Logic ---
# Reset if new audio file is uploaded
if audio_file and st.session_state.get("audio_file_name") != audio_file.name:
    st.session_state.audio_file_name = audio_file.name
    clear_editor_widget_state(st.session_state.num_lyrics_lines)
    st.session_state.lyrics = []
    st.session_state.sync_times = []
    st.session_state.lyrics_file_name = None
    st.session_state.num_lyrics_lines = 0
    st.rerun()

# Reset and load new lyrics if new lyrics file is uploaded
if lyrics_file and (st.session_state.lyrics_file_name != lyrics_file.name):
    clear_editor_widget_state(st.session_state.num_lyrics_lines)
    st.session_state.lyrics_file_name = lyrics_file.name
    lyrics_content = lyrics_file.read().decode("utf-8")
    st.session_state.lyrics = [
        line.strip() for line in lyrics_content.splitlines() if line.strip()
    ]
    st.session_state.sync_times = [""] * len(st.session_state.lyrics)
    st.session_state.num_lyrics_lines = len(st.session_state.lyrics)
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
if audio_file:
    # Initialize with a single empty line if no lyrics are present
    if not st.session_state.lyrics:
        st.session_state.lyrics = [""]
        st.session_state.sync_times = [""]
        st.session_state.num_lyrics_lines = 1

    st.write("Edit lyrics, add/remove lines, and click 'Set' to capture timestamps.")

    col1, col2, col3 = st.columns([7, 3, 2], gap="small")
    col1.write("**Lyric Text**")
    col2.write("**Timestamp (mm:ss.ms)**")
    col3.write("**Actions**")

    for i in range(len(st.session_state.lyrics)):
        with col1:
            st.text_input(
                "Lyric",
                value=st.session_state.lyrics[i],
                key=f"lyric_{i}",
                label_visibility="collapsed",
            )
        with col2:
            st.text_input(
                "Timestamp",
                value=st.session_state.sync_times[i],
                key=f"timestamp_{i}",
                label_visibility="collapsed",
            )
        with col3:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Set", key=f"set_{i}", use_container_width=True):
                    persist_editor_state()
                    current_time = st.session_state.get("waveform_player", 0.0)
                    minutes = int(current_time // 60)
                    seconds = int(current_time % 60)
                    milliseconds = int((current_time % 1) * 1000)
                    st.session_state.sync_times[i] = (
                        f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                    )
                    st.rerun()
            with b2:
                if st.button("Del", key=f"delete_{i}", use_container_width=True):
                    persist_editor_state()
                    st.session_state.lyrics.pop(i)
                    st.session_state.sync_times.pop(i)
                    st.session_state.num_lyrics_lines = len(st.session_state.lyrics)
                    clear_editor_widget_state(st.session_state.num_lyrics_lines + 1)
                    st.rerun()

    st.write("")  # Spacer
    if st.button("+ Add New Lyric"):
        persist_editor_state()
        st.session_state.lyrics.append("")
        st.session_state.sync_times.append("")
        st.session_state.num_lyrics_lines = len(st.session_state.lyrics)
        st.rerun()

else:
    st.info("Upload an audio file to begin syncing lyrics.")

# --- 5. Export Synced Lyrics Section ---
st.header("5. Export Synced Lyrics")
if st.session_state.lyrics and any(t for t in st.session_state.sync_times):
    persist_editor_state()  # Save any last-minute edits

    # Generate LRC content
    lrc_content = []
    for i, lyric in enumerate(st.session_state.lyrics):
        timestamp = st.session_state.sync_times[i]
        if timestamp and is_valid_timestamp_format(timestamp):
            if "." in timestamp:
                parts = timestamp.split(".")
                ms = parts[1]
                xx = ms.ljust(2, "0")[:2]
                formatted_timestamp = f"{parts[0]}.{xx}"
            else:
                formatted_timestamp = f"{timestamp}.00"

            lrc_content.append(f"[{formatted_timestamp}]{lyric}")

    lrc_string = "\n".join(lrc_content)

    file_name = "lyrics.lrc"
    if st.session_state.get("audio_file_name"):
        base_name, _ = os.path.splitext(st.session_state.audio_file_name)
        file_name = f"{base_name}.lrc"

    st.download_button(
        label="Download .lrc file",
        data=lrc_string,
        file_name=file_name,
        mime="text/plain",
    )
else:
    st.info("Sync at least one lyric line to enable export.")

# --- Sidebar: About/Help ---
with st.sidebar:
    st.markdown("## About")
    st.markdown("""
    This app helps you manually sync lyrics to music for karaoke or lyric videos.
    - Built with [Streamlit](https://streamlit.io/)
    """)
    st.markdown("**MVP Version** - core features only.")

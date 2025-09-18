# Project Handover Notes

## Current Status

The core functionality of the Synced Lyrics Generator is complete and working. Users can:
- Upload an audio file.
- Upload a .txt lyrics file or manage lyrics manually (add, edit, delete lines).
- Interact with a waveform player (play, pause, change speed, scrub).
- Assign the player's current time to each lyric line with a "Set" button.
- Export the final synced lyrics as a standard .lrc file.

The application state is managed carefully to allow for interactive edits without data loss.

---

## Unfinished Work & Next Steps

### Active Lyric Highlighting (High Priority)

The original project plan included highlighting the lyric line that is currently active during audio playback. This feature is not implemented.

**To-Do:**
- The `wavesurfer_player` component already sends the current playback time to the Streamlit backend (it's stored in `st.session_state.wavesurfer_player`).
- The Python script needs to use this time to determine which lyric's timestamp has just passed.
- The UI should then be updated to visually distinguish that "active" lyric line (e.g., by changing its background color or using `st.markdown` with bold text).

### Code and Component Maintenance

- **Component Build Process:** The custom component in `components/wavesurfer_player/` (package name updated to `streamlit-wavesurfer-player`) has a frontend part that requires a manual build step after any changes. To modify it, navigate to `components/wavesurfer_player/wavesurfer_player/frontend` and run `npm install` (if needed) and `npm run build`.
- **State Management:** The state handling in `app.py` (specifically the `persist_editor_state()` function and the logic inside button clicks) is complex. It works, but any new interactive elements will need to be integrated carefully to avoid breaking the state flow.

---

## Known Issues

- There are no known bugs at this time. The application appears stable.

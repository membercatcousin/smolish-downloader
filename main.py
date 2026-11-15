import re
import urllib.request
import streamlit as st

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)"}

st.set_page_config(page_title="Smolish Downloader", page_icon="🎬", layout="centered")
st.title("Smolish Downloader")
st.caption("Download Smolish videos without the watermark.")

url = st.text_input("Paste a Smolish link", placeholder="https://smolish.com/v/...")

if url:
    url = url.strip()
    if not url.startswith("https://smolish.com/"):
        st.error("Please enter a valid https://smolish.com/ link.")
    else:
        try:
            with st.spinner("Grabbing video..."):
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=10) as page:
                    html = page.read().decode("utf-8", "ignore")

            match = re.search(r'https://cdn\.smolish\.com/videos/(\d+)/[^"\'\s<>]+\.mp4', html)
            if not match:
                st.error("Couldn't find a video on that page.")
            else:
                vid_url, vid_id = match.group(0), match.group(1)
                st.video(vid_url)

                def fetch_video():
                    with urllib.request.urlopen(
                        urllib.request.Request(vid_url, headers=HEADERS), timeout=30
                    ) as r:
                        return r.read()

                st.download_button(
                    label="Download MP4",
                    data=fetch_video,
                    file_name=f"smolish_{vid_id}.mp4",
                    mime="video/mp4",
                    type="primary",
                )
        except Exception as e:
            st.error(f"Failed to fetch video: {e}")

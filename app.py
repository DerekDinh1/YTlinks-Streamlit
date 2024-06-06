import streamlit as st
from getPlaylistInfo import get_playlist_info
from getChannelInfo import get_channel_info

st.title('Welcome to YTLinkIt!')
st.divider()

# Form for Channel Link
channel_form = st.form(key='channel_form')
with channel_form:
  st.header('Channel Link')
  channel_input = st.text_input('Enter URL of Channel:')
  channel_submit_button = channel_form.form_submit_button('Get Channel Info')

if channel_submit_button and channel_input:
  get_channel_info(channel_input)

# Form for Playlist Link
playlist_form = st.form(key='playlist_form')
with playlist_form:
  st.header('Playlist Link')
  playlist_input = st.text_input('Enter URL of Playlist:')
  playlist_submit_button = playlist_form.form_submit_button('Get Playlist Info')

if playlist_submit_button and playlist_input:
  get_playlist_info(playlist_input)
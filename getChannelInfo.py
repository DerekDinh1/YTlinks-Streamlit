import os
from pytube import Channel, exceptions
import streamlit as st

# Ensure pytube is installed and imported
try:
    from pytube import Channel
except ModuleNotFoundError:
    os.system('pip install pytube')

def get_channel_info(channel_input):
    try:
        # Function to get channel URL from user URL
        def get_channel_url(user_url):
            # Extract the username
            username = user_url.split('@')[-1]
            # Construct the URL to fetch the channel details
            return f"https://www.youtube.com/c/{username}"

        # Check if the URL is a user or channel URL
        if '@' in channel_input:
            # Convert the user URL to the channel URL
            channel_url = get_channel_url(channel_input)
        else:
            channel_url = channel_input

        channel = Channel(channel_url)
        
        st.divider()

        # Displays channel data
        st.write('### Channel Info')
        st.write(f'**Channel Name:** {channel.channel_name}')
        st.write(f'**Channel ID:** {channel.channel_id}')
        st.write(f'**Channel Owner:** {channel.channel_url}')  # Assuming channel_url is the owner. Adjust if needed.
    except exceptions.RegexMatchError:
        st.write('The provided URL does not match any channel. Please check the URL and try again.')
    except Exception as e:
        st.write(f'An unexpected error occurred: {e}')
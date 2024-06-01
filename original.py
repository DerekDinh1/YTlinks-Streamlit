import os
import io
import pandas as pd
import streamlit as st
from pytube import Playlist, YouTube, exceptions

# Adding commented code below as a reminder to use when ready for databases to cache data
#@st.cache(allow_output_mutation=True)

# Ensure pytube is installed and imported
try:
    from pytube import Playlist, YouTube
except ModuleNotFoundError:
    os.system('pip install pytube')

st.title('Welcome to YTLinkIt!')
st.divider()

# Input link as a form
playlist_form = st.form(key = 'Playlist_form')
with playlist_form.header('Playlist Link'):
  playlist_input = st.text_input('Enter URL of Playlist:')
  form_submit_button1 = playlist_form.form_submit_button('Enter')

if playlist_input:
  try:
    vid_links = Playlist(playlist_input)

    st.divider()

    # Displays playlist data
    display_data =  st.write( '# Playlist Info\n',
                              '#### Playlist Title: \n', vid_links.title,
                              '\n#### Number of Videos:\n', vid_links.length, 
                              '\n#### Playlist ID:\n', vid_links._playlist_id)

    # Get video data
    video_data = []
    
    for link in vid_links.video_urls:
      try:
        yt = YouTube(link)
        video_data.append({'Title': yt.title, 'Link': link})
      except exceptions.VideoUnavailable:
        st.write(f'Video {link} is unavailable. Skipping.')
      except Exception as e:
        st.write(f'An error occurred with video {link}: {e}')

    dataframe = pd.DataFrame(video_data)

    # Turns data into a .csv file in memory
    csv_buffer = io.BytesIO()
    dataframe.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    st.divider()

    st.write('### Success! Good job, you did it.\n')
    
    # Read the CSV file to provide it as a downloadable link
    st.download_button(
      label = 'Download CSV',
      data = csv_buffer,
      file_name = f'{vid_links.title}.csv',
      mime = 'text/csv'
    )
      
  except exceptions.RegexMatchError:
    st.write('The provided URL does not match any playlist. Please check the URL and try again.')
  except exceptions.ExtractError:
    st.write('There was an error extracting information from the playlist. The playlist might be private or invalid.')
  except Exception as e:
    st.write(f'An unexpected error occurred: {e}')
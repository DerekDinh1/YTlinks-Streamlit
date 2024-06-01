import os
import io
import pandas as pd
import streamlit as st
from pytube import Playlist, YouTube, exceptions

# Ensure pytube is installed and imported
try:
    from pytube import Playlist, YouTube
except ModuleNotFoundError:
    os.system('pip install pytube')

def get_playlist_info(playlist_input):
    if playlist_input:
        try:
            vid_links = Playlist(playlist_input)
            st.divider()

            # Displays playlist data
            st.write('# Playlist Info\n',
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

            st.write('### Success! Good job, you did it.')
            
            # Create a download button for the CSV file
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

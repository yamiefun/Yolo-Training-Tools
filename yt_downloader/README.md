# Youtube Downloader

This tool can help you to download videos or live streams on Youtube and parse them into frames to generate dataset images.

## Usage

1. Create [Conda](https://docs.conda.io/en/latest/) environment with the given `.yml` file.

    ```
    conda env create -f environments.yml
    ```

2. Activate environment and install `pafy` manually.

    ```
    conda activate yt_downloader
    pip3 install install git+https://github.com/mps-youtube/pafy
    ```

3. Modify `config.json`.
    
    Short explanations:
    + `url`: Video url.

    + `url_type`: "youtube" or "youtube-dl".

    + `folder_name`: Folder that all frames will be stored into. It will be placed under `dataset` folder automatically. 

    + `is_live`: Is the youtube video live or not, should be `true` or `false`.

    + `extract_frames_per_second`: How many frames do you want to extract per second, should be an integer.

    Detail:
    
    You can try to directly paste youtube link to the `url` field, and fill "youtube" into `url_type`. If this is not working, you can follow the below steps to convert youtube url to downloaded url.
    
    1.  ```
        youtube-dl --list-formats <youtube url>
        # ex:
        $ youtube-dl --list-formats https://youtu.be/GQVs1EN3Si4
        [youtube] GQVs1EN3Si4: Downloading webpage
        [youtube] GQVs1EN3Si4: Downloading m3u8 information
        [youtube] GQVs1EN3Si4: Downloading MPD manifest
        [info] Available formats for GQVs1EN3Si4:
        format code  extension  resolution note
        91           mp4        256x144     290k , avc1.42c00b, 15.0fps, mp4a.40.5
        92           mp4        426x240     546k , avc1.4d4015, 30.0fps, mp4a.40.5
        93           mp4        640x360    1209k , avc1.4d401e, 30.0fps, mp4a.40.2
        94           mp4        854x480    1568k , avc1.4d401f, 30.0fps, mp4a.40.2
        95           mp4        1280x720   2969k , avc1.4d401f, 30.0fps, mp4a.40.2 (best)
        ```

    2. Select a format code that you prefer, then execute the command below.

        ```
        youtube-dl --format <format code> --get-url <youtube url>
        # ex:
        $ youtube-dl --format 95 --get-url https://youtu.be/GQVs1EN3Si4
        https://manifest.googlevideo.com/api/manifest/...
        ```

        The output will be a downloaded url. You can paste the url into the `url` field, and fill "youtube-dl" into `url_type`.

4. Now you can easily run the code by

    ```
    python3 yt_downloader.py --config <config file>
    # ex:
    python3 yt_downloader.py --config config.json
    ```
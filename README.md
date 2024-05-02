# YouTube Scraper


This app will help you to scrap data of any particular YouTube channel, you can scrape titles, views, likes, date of publish and the video url, and all these data will be saved in a csv file.


*Note: For this application to function properly in your local system, ensure that the required dependencies are installed and configured correctly, and make sure that you have your Google API Key.*

### Create Virtual Environment 
- `python3 -m venv venv` - Ubuntu/MacOs
- `python -m venv venv` - Windows

### Activate the environment
- `source venv/bin/activate`  - Ubuntu/MaOS
- `venv/Script/acitvate` - Windows

### Installing Dependencies
- `pip3 install -r requirements.txt`- Ubuntu/MacOs
- `pip install -r requirements.txt` - Windows

### create environment variable
- create a .env file
- Inside the .env file create a variable name as `YT_API_KEY` and store your key inside this variable.


### Run the script
`python yt_scrapper.py`


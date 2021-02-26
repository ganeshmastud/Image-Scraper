# Image Scraper
images are Scrap from the google chrome.
Selenium WebDriver is used to make requests to the google search images after iamges loaded, click action perform on the each image thumbnail after the images is open the iamge url is stored in list.
Each url is fetch from the list and checked if it contains https.If it contains then the content or the url is stored in list and after that it is written in the given folder path.

input to search images is taken from index page and then pass to the show image function in app.py, then the input is send to search_and_download function form which images are fetch and store in folder and then those images
shown on the webpage

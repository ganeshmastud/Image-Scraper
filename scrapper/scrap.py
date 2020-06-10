import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def fetch_img_urls(search_term,max_img, driver, sleep_between_interactions):
	search_url="https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
	# load the page
	driver.get(search_url.format(q=search_term))
	image_urls = set()
	image_count = 0
	results_start = 0
	while image_count < max_img:
		
		scroll_to_end(driver)
		thumbnail_results = driver.find_elements_by_css_selector("img.Q4LuWd")
		number_results = len(thumbnail_results)
		print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
		for img in thumbnail_results[results_start:number_results]:
			# try to click every thumbnail such that we can get the real image behind it
			try:
				img.click()
				time.sleep(sleep_between_interactions)
			except Exception:
				continue

			# extract image urls
			actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
			for actual_image in actual_images:
				if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
					image_urls.add(actual_image.get_attribute('src'))

			image_count = len(image_urls)

			if len(image_urls) >= max_img:
				print(f"Found: {len(image_urls)} image links, done!")
				break
			else:
				print("Found:", len(image_urls), "image links, looking for more ...")
				#time.sleep(0.5)
			  
			load_more_button = driver.find_element_by_css_selector(".mye4qd")
			if load_more_button:
				driver.execute_script("document.querySelector('.mye4qd').click();")

				# move the result startpoint further down
			results_start = len(thumbnail_results)

	return image_urls


def persist_img(folder_path:str,url:str, counter):
	try:
		image_content = requests.get(url).content

	except Exception as e:
		print(f"ERROR - Could not download {url} - {e}")

	try:
		f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
		f.write(image_content)
		f.close()
		print(f"SUCCESS - saved {url} - as {folder_path}")
	except Exception as e:
		print(f"ERROR - Could not save {url} - {e}")

def fetch_img(search_term,target_path):
	folder_name = target_path
	file = search_term
	img_folder = folder_name + '/' + file
	list_of_folders = os.listdir(folder_name)
	list_ofimgs = []
	for i in list_of_folders:

		if i == file:
			images = os.listdir(img_folder)
			for j in images:
				list_ofimgs.append(j)
	if len(list_ofimgs)==0:
		return 0

	return list_ofimgs
def search_and_download_image(search_term: str, drive_path: str, target_path='./static',max_img=15):
	target_folder= os.path.join(target_path, '_'.join(search_term.lower().split()))
	
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)
	with webdriver.Chrome(executable_path=drive_path) as driver:
		res=fetch_img_urls(search_term,max_img, driver, sleep_between_interactions=1)

	cnt=0
	for elem in res:
		persist_img(target_folder,elem,cnt)
		cnt+=1

	list_imgs= fetch_img(search_term,target_path)
	return list_imgs
# drive_path='./chromedriver'
# search_term=input()
#driver = webdriver.Chrome() 
#driver.maximize_window()  
#driver.get("https://www.google.com/search?q="+search_term+"&tbm=isch")


# search_and_download_image(search_term,drive_path)
#sleep_between_interactions=1


#target_path='./images'
'''
target_folder= os.path.join(target_path, '_'.join(search_term.lower().split()))
if not os.path.exists(target_folder):
	os.makedirs(target_folder)
with webdriver.Chrome(executable_path=drive_path) as driver:
	res=fetch_img_urls(search_term,max_img,driver, sleep_between_interactions)

cnt=0
for elem in res:
	persist_img(target_folder,elem,cnt)
	cnt+=1'''

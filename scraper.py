from bs4 import BeautifulSoup as bs
from requests import get
from skimage import io
import cv2, os

search = input("Enter search title: ").title()

# get current working directory
path = os.getcwd()

# create a folder with the search title
folder = os.path.join(path, search)

if os.path.isdir(folder): print(f"Folder with the name {search} already exists!")
else: 
    os.mkdir(folder)
    print(f"Folder with the name {search} created!")

# get the html of the search page
url = f"https://www.google.com/search?q={search}&tbm=isch"
page = get(url)
soup = bs(page.text, "html.parser")

# get all the images
images = soup.find_all("img")[1:]

# download the images
for index, image in enumerate(images):
    link = image.get("src") # get the link of the image
    img = io.imread(link)

    # dimensions of the image (high, width, channels)
    hight, width, _ = img.shape # _ is a dummy variable

    # resize the image thrice of its original size
    img = cv2.resize(img, (width*3, hight*3))

    # convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imshow(search, img)

    # image name and path
    image_path = os.path.join(folder, f"{search}{index}.jpg")
    
    # save the image
    print(f"Saving to {image_path}")
    cv2.imwrite(image_path, img)

    # wait for 100ms and if q is pressed then break
    if cv2.waitKey(100) == ord("q"):
        break

# destroy all the windows
cv2.destroyAllWindows()

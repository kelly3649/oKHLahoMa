import requests
import base64

image = "data:image/jpg," + base64.b64encode(open("image.jpg", "rb").read())

print image
url = "https://api.cloudinary.com/v1_1/dhan3kbrs/image/upload"

images = [ ('images', ('image.png', open('image.png', 'rb'), 'image/png'))]

requestobject = requests.post(url, params = {"file" : image})
print requestobject.text

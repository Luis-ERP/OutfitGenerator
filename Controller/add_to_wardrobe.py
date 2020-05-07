import numpy as np 
import random
import matplotlib.pyplot as plt
import json

from collections import Counter
from sklearn.cluster import KMeans
import cv2

##				  string   string	 int		int		  int      bool          bool  					False
def addToWardrobe(imgUrl, category, width, height, nuColors=9, plot=True, returnPalette=False, returnWardrobeLength=False):

	## PREPROCESSING ---------------------------------------------------------------------------------------
	img = cv2.imread(imgUrl)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = cv2.resize(img, dsize=(width, height))
	#img = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT)


	## FOREGROUND EXTRACTION ---------------------------------------------------------------------------------------
	mask = np.zeros(img.shape[:2], np.uint8)
	bgModel = np.zeros((1,65), np.float64)
	fgModel = np.zeros((1,65), np.float64)

	#rect = (5, 5, int(width*0.95), int (height-0.95))
	#rect = (10, 10, int(width-(width*.2)), int(height-(width*.2)))
	rect = (1, 1, width-10, height-10)
	cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
	mask2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')

	fgImg = img * mask2[:,:,np.newaxis]

	if plot: #just plot
		plt.imshow(fgImg)
		plt.show()


	## COLOR PALETTE ---------------------------------------------------------------------------------------
	imgColors = fgImg.reshape(fgImg.shape[0]*fgImg.shape[1], 3) #flatten
	
	#	cluster main colors
	clf = KMeans(n_clusters=nuColors)
	targets = clf.fit_predict(imgColors)
	counts = Counter(targets)
	counts[0] = 0
	centerColors = clf.cluster_centers_
	orderedColors = [centerColors[i] for i in counts.keys()]
	rgbColors = [orderedColors[i] for i in counts.keys()]
	totalAmount = sum([counts[i] for i in counts.keys()])
	for i in counts.keys():
		if counts[i]/totalAmount >= .6:
			addToWardrobe(imgUrl, category, width, height, nuColors, plot)
			return

	if plot: # just plot
		def rgb2hex(color):
			return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
		hexColors = [rgb2hex(orderedColors[i]) for i in counts.keys()]
		plt.figure(figsize=(8,6))
		plt.pie(counts.values(), labels=hexColors, colors=hexColors)
		plt.show()

	#convert to HSV
	def rgb2hsv(r,g,b):
		r, g, b = r/255.0, g/255.0, b/255.0
		mx = max(r, g, b)
		mn = min(r, g, b)
		df = mx-mn
		if mx == mn:
			h = 0
		elif mx == r:
			h = (60 * ((g-b)/df) + 360) % 360
		elif mx == g:
			h = (60 * ((b-r)/df) + 120) % 360
		elif mx == b:
			h = (60 * ((r-g)/df) + 240) % 360
		if mx == 0:
			s = 0
		else:
			s = (df/mx)*100
		v = mx*100
		return [h/360, s/100, v/100] #normalized

	#convert to hsv
	hsvColors = []
	for i in range(len(rgbColors)):
		hsvColors.append(rgb2hsv(rgbColors[i][0],rgbColors[i][1],rgbColors[i][2]))

	#create palette
	palette = []
	for i in range(len(hsvColors)):
		palette.append(hsvColors[i])
	del palette[0]

	if returnPalette:
		return palette

		
	## GET CATEGORIES ---------------------------------------------------------------------------------------
	with open('../DataBase/categories.json') as f:
		categories = json.load(f)

	attributes = None
	formalSpecific = None
	for group in categories['groups']:
		if group['group'] == category:
			attributes = group['attributes']
			formalSpecific = group['formal_specific']
			break

	## GENERATE ID ---------------------------------------------------------------------------------------
	def unique_id():
		seed = random.getrandbits(32)
		while True:
			yield seed
			seed += 1

	_id = next(unique_id())

	## ADD ALL INFORMATION TO DATABASE ---------------------------------------------------------------------------------------
	currentWardrobe = {}
	try:
		with open('../DataBase/wardrobe.json') as f:
			currentWardrobe = json.load(f)
	except:
		currentWardrobe = []
	#																					replace with: formalSpecific
	new = {'id': _id, 'name': imgUrl, 'palette': palette, 'attributes': attributes, 'formal_specific': [-1, 1]}
	currentWardrobe.append(new)

	with open('../DataBase/wardrobe.json', 'w') as f:
		json.dump(currentWardrobe, f)

	if returnWardrobeLength:
		return len(currentWardrobe)


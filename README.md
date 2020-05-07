# OutfitGenerator
Prototype of a mobile application using ML and DL to create outfits based on your current wardrobe and your preferences.

This is the prototype of a mobile application I am currently developing. I started this project because I realized I wasn't good choosing my clothes to go to HighSchool so I decided that an algorithm should do it for me! I it developed in Python 3 and it uses Machine Learning to select the best fit. I made used of the well-know library OpenCV to process the images, with the help of SciKit Learn. The project is divided mainly into two parts, the first one is to upload the image of a garment and save it to use it in the second part. Which is to find the best combinations posible to get a nice outfit.

The logic behind the first part is:
1) It process the image so it is only the garment without the background
2) The image is blured so only the main colors are picked
3) Get the main n colors of the garment. This is achieved by making use of a clustering ML algorithm
4) Store the colors with some extra information so the it can be used later

The logic behind the second part is:
1) Pick a random upper garment (shirt, t-shirt, etc.) from storage
2) Pick a lower garment (jeans, trousers, etc.) as the color is in harmony with the upper gament selected
3) Pick the rest of the items (shoes, belts, necklace, etc.) according to the other garments selected
4) Display the result

"""
The following script was used to convert the original folder into a YOLOv5 friendly format.

Only needs to be run once. Assumes data was downloaded into the current directory

"""
import random
import os
import shutil
import glob
from PIL import Image, ImageDraw

def show_bbox(image_path):
	# convert image path to label path
	label_path = image_path.replace('.jpg', '.txt')

	# Open the image and create ImageDraw object for drawing
	image = Image.open(image_path)
	draw = ImageDraw.Draw(image)

	with open(label_path, 'r') as f:
		for line in f.readlines():
			# Split the line into five values
			label, x, y, w, h = line.split(' ')

			# Convert string into float
			x = float(x)
			y = float(y)
			w = float(w)
			h = float(h)

			# Convert center position, width, height into
			# top-left and bottom-right coordinates
			W, H = image.size
			x1 = (x - w/2) * W
			y1 = (y - h/2) * H
			x2 = (x + w/2) * W
			y2 = (y + h/2) * H

			# Draw the bounding box with red lines
			draw.rectangle((x1, y1, x2, y2),
						   outline=(255, 0, 0), # Red in RGB
						   width=3)             # Line width
	image.show()

def get_filenames(folder):
	filenames = []
	
	for path in glob.glob(os.path.join(folder, '*.jpg')):
		# Extract the filename
		filename = os.path.split(path)[-1]        
		filenames.append(filename)

	return filenames


def split_dataset(image_names, train_size, val_size):
	for i, image_name in enumerate(image_names):
		# Label filename
		label_name = image_name.replace('.jpg', '.txt')
		
		# Split into train, val, or test
		if i < train_size:
			split = 'train'
		elif i < train_size + val_size:
			split = 'val'
		else:
			split = 'test'
		
		# Source paths
		source_image_path = image_name
		source_label_path = label_name

		# Destination paths
		target_image_folder = f'data/images/{split}'
		target_label_folder = f'data/labels/{split}'

		# Move files
		shutil.move(source_image_path, target_image_folder)
		shutil.move(source_label_path, target_label_folder)

if __name__ == "__main__":

	# Create a folder structure for YOLOv5 training
	if not os.path.exists('data'):
		for folder in ['images', 'labels']:
			for split in ['train', 'val', 'test']:
				os.makedirs(f'data/{folder}/{split}')

	images = get_filenames(".")
	# Cat data
	random.shuffle(images)
	N = len(images)
	split_dataset(images, train_size=int(0.8 * N), val_size=int(0.1 * N)) # 80 10 10 train-val-test split
	
	
	
# Datasets
A folder with small datasets that we have.
- kaggle_traffic_sign -> Downloaded from https://www.kaggle.com/code/hemraj12/traffic-signs-detection-on-carla-simulator/data?select=ts
	- ran `script.py` for YOLOv5 friendly file structure
	- Added `data.yml`
	
	
### YOLOv5 training
python3 train.py --data /datasets/kaggle_traffic_sign/data.yaml --weights yolov5s.pt --epochs 100 --batch 4 --freeze 10
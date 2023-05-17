The model is trained to classify these classes

`["land slide","drought","urban fire","infrastructure","flooding","earthquake","wild fire"]`

We use this model and thresholding to determine the spam image (Image that is not one of these classes).

`train.ipynb` => training code

`find_thresholds.ipynb` => thresholding code to find best thresholds for each class.

# API

API for classification located in folder `api`. Use `docker build` and `docker run` to run the API in docker environment.




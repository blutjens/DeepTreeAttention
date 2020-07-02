#Experiment
import glob
import os
from comet_ml import Experiment
from DeepTreeAttention.main import AttentionModel
from DeepTreeAttention.visualization import visualize
from datetime import datetime
import matplotlib.pyplot as plt

experiment = Experiment(project_name="deeptreeattention", workspace="bw4sz")

#timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
experiment.log_parameter("timestamp",timestamp)

#Create a class and run
model = AttentionModel()
model.create(name="single_conv")
model.read_data()
    
#Log config
experiment.log_parameters(model.config["train"])
experiment.log_parameter("Training Batch Size", model.config["train"]["batch_size"])

model.train()

#Predicted raster
predict_tfrecords = glob.glob("/orange/ewhite/b.weinstein/Houston2018/tfrecords/predict/*.tfrecord")
results = model.predict(predict_tfrecords, batch_size=200)
predicted_raster = visualize.create_raster(results)

save_dir = "{}/{}".format("/orange/ewhite/b.weinstein/Houston2018/snapshots/",timestamp)
os.mkdir(save_dir)
prediction_path = "{}/predicted_raster.png".format(save_dir)
experiment.log_image(name="Prediction", image_data=predicted_raster, image_colormap=visualize.discrete_cmap(20, base_cmap="jet"))

#Save model
model.model.save("{}/{}.h5".format(save_dir,timestamp))
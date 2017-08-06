# -*- coding: utf-8 -*-

import pandas as pd
import time

from uchidata import Uchidata

# Credentials
uchidata_url = "API URL"
my_key = "API KEY"

# Set model name and load data
model_name = "ag_news"

d_train = pd.read_csv('ag_news_train.csv')
d_test = pd.read_csv('ag_news_test.csv')

# Initialise Uchidata client
uchidata = Uchidata(api_url = uchidata_url, api_key = my_key)

# Send training dataset
uchidata.send_training_data(model = model_name, dataset = d_train, y_var="target", id_var = "observation_id", echo=True)

# Learn model
uchidata.learn_model(model=model_name)

# Check model status every 30s until the model is ready
model_status = uchidata.check_status(model=model_name)

while "ready" not in model_status["message"]:
    print(model_status["message"])
    time.sleep(30)
    model_status = uchidata.check_status(model=model_name)


# Load model
uchidata.load_model(model=model_name)

# Compute predictions
preds = uchidata.predict(model=model_name, dataset=d_test, n_predictions = 2, id_var = "observation_id") 
print("predictions computed")

# Close model
uchidata.close_model(model=model_name)
print("model closed")

# Compute accuracy
y_pred = [p['predictions']['top1']['label'] for p in preds['result']['output']]
acc = [1*(y_pred[i] == str(y)) for i,y in enumerate(d_test["target"])]
accuracy = sum(acc)/float(len(y_pred))
print("accuracy:" + str(accuracy))

# Analyze predictions (number of predictions and proportion predicted in each category)
stats_predictions = uchidata.analyze_predictions(model_name)
print(stats_predictions)

# Remove model
uchidata.remove_model(model_name)


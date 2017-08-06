# Uchidata starter kit

Uchidata is a Natural Language Processing API for Text-Classification in real-time.

Here we will see how to install Uchidata and dependencies, download data to reproduce ag_news benchmark, and a sample python code to send requests to the API.

### Install

Install git and clone repo

```shell
sudo apt-get install git
git clone https://github.com/uchidata/python-example.git
```

Install pip and python dependencies

```shell
sudo apt-get install python-pip
sudo pip install pandas
sudo pip install requests
```

### Download data
```shell
cd python-example
wget "https://s3-us-west-2.amazonaws.com/uchidata-demo/ag_news_test.csv"
wget "https://s3-us-west-2.amazonaws.com/uchidata-demo/ag_news_train.csv"
```

### Reproduce Ag_news benchmark

1. Add your API key and API url in the python script.

2. Run python_example.py
 
```shell
python python_example.py
```

# API Functions

### send_training_data
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"send_training_data",
  "model":"MODEL NAME",
  "data":[
          {"y":"label1", "id":1, "var1":"VALUE OF VARIABLE 1", "var2":"VALUE OF VARIABLE 1", ...}, 
          {"y":"label2", "id":2, "var1":"VALUE OF VARIABLE 1", "var2":"VALUE OF VARIABLE 1", ...}
         ]
}
```

Output

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message": "Model 'MODEL NAME': n observations added in the training set (total:N observations)"
}
```

### learn_model
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"learn_model",
  "model":"MODEL NAME"
}
```

Output

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message": "Model 'MODEL NAME' is training"
}
```

### check_status
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"get_status",
  "model":"MODEL NAME"
}
```

Output

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message": MODEL STATUS
}
```

### load_model
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"load_model",
  "model":"MODEL NAME"
}
```

Output

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message":  "Model 'MODEL NAME' is in memory and ready to compute predictions"
}
```

### predict
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"predict",
  "model":"MODEL NAME",
  "n_predictions":n, # Output n predictions per observation
  "data":[
          {"id":1, "var1":"CONTENT OF VARIABLE 1", "var2":"CONTENT OF VARIABLE 1", ...}, 
          {"id":2, "var1":"CONTENT OF VARIABLE 1", "var2":"CONTENT OF VARIABLE 1", ...}
         ]
}
```

Output: example with n_predictions = 3

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message": "Predictions have been computed",
  "result":
    {
      "model": "MODEL NAME",
      "n": 3,
      "output": 
        [
          {
            "id": "1", 
            "predictions": 
              {
                "top1": {"score": 0.7196, "label": "label3"},
                "top2": {"score": 0.6721, "label": "label1"}, 
                "top3": {"score": 0.2742, "label": "label2"}, 
              }
          }, 
          {
            "id":"2", 
            "predictions": 
              {
                "top1": {"score": 0.6152, "label": "label3"}, 
                "top2": {"score": 0.7817, "label": "label4"},
                "top3": {"score": 0.1837, "label": "label1"}
              }
          }
        ]
    }
}
```

### close_model
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"close_model",
  "model":"MODEL NAME"
}
```

Output

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message":  "Model 'MODEL NAME' is closed. Use method 'load_model' before computing new predictions."
}
```

### analyze_predictions
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"analyze_predictions",
  "model":"MODEL NAME"
}
```

Output

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message":  "Statistics on predictions have been computed.",
  "stats":
    {
      "n_total":12345, # Total number of predictions computed
      "n_last_batch":123, # Number of predictions in the last batch
      "last_batch": # Proportion of each label
        {
          "label1":0.567,
          "label2":0.213,
          "label3":0.123,
          "label4":0.097
        }
    }
}
```

### remove_model
Input

```json
{
  "api_key":"YOUR API KEY",
  "function":"remove_model",
  "model":"MODEL NAME"
}
```

Output

```json
{
  "timestamp": "2017-08-06 00:54:51", 
  "message":  "Model 'MODEL NAME' removed."
}
```



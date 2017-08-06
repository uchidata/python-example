# -*- coding: utf-8 -*-

import json
import requests

class Uchidata():
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def send_training_data(self, model, dataset, y_var, id_var = None, echo = False):
        """
        Input:
          model: name of the model
          dataset: a dataframe with training observations
          y_var: name of the target variable
          id_var: name of the variable id
          echo: True to print information
        """
        if list(dataset) == range(0,dataset.shape[1]):
            return "TRAINING DATA NOT SENT: Please specify column names"
            
        if y_var not in list(dataset):
            return "TRAINING DATA NOT SENT: variable '" + y_var + "' not found"
        else:
            y_pos = list(dataset).index(y_var)
            
        if id_var is not None:
            if id_var not in list(dataset):
                return "TRAINING DATA NOT SENT: variable '" + id_var + "' not found"
            else:
                id_pos = list(dataset).index(id_var)
        else:
            id_pos = None

        d = {}
        d['api_key'] = self.api_key
        d['function'] = "send_training_data"
        d['model'] = model
        d['data'] = []
        
        n = 0
        while n < dataset.shape[0]:
            # Build new observation
            if id_pos is not None:
                new_obs = {'id':dataset[id_var][n], 'y':dataset[y_var][n]}
            else:
                new_obs = {'id':n, 'y':dataset[y_var][n]}
                
            for i, name_var in enumerate(list(dataset)):
                if i not in [y_pos, id_pos]:
                    new_obs[name_var] = dataset[name_var][n]
                
            # Add new observation
            d['data'].append(new_obs)
            
            # Send batch of 5000 observations
            if (n+1) % 5000 == 0:
                try:
                    result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
                    d['data'] = []
                    if echo:
                        print('n = ' + str(n) + ' / ' + str(dataset.shape[0]) + ' observations added to the training set')
                except:
                    print('n = ' + str(n) + ' / ' + str(dataset.shape[0]) + ' - ERROR ')
            n += 1
            
        # Send the last batch of observations
        if (n+1) % 5000 != 1:
            result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))

        return json.loads(result.content)

    def learn_model(self, model):
        """
        Input:
          model: name of the model
        """
        d = {}
        d['api_key'] = self.api_key
        d['function'] = 'learn_model'
        d['model'] = model
        result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
        return json.loads(result.content)
    
    def remove_model(self, model):
        """
        Input:
          model: name of the model
        """
        d = {}
        d['api_key'] = self.api_key
        d['function'] = 'rm_model'
        d['model'] = model
        result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
        return json.loads(result.content)
    
    def check_status(self, model):
        """
        Input:
          model: name of the model
        """
        d = {}
        d['api_key'] = self.api_key
        d['model'] = model
        d['function'] = 'get_status'
        
        result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
        return json.loads(result.content)

    def load_model(self, model):
        """
        Input:
          model: name of the model
        """
        d = {}
        d['api_key'] = self.api_key
        d['model'] = model
        d['function'] = 'load_model'
        result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
        return json.loads(result.content)
        
    def close_model(self, model):
        """
        Input:
          model: name of the model
        """
        d = {}
        d['api_key'] = self.api_key
        d['model'] = model
        d['function'] = 'close_model'
        result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
        return json.loads(result.content)
        
    def predict(self, model, dataset, id_var = None, n_predictions = 1, output_type = 'probs'):
        """
        Input:
          model: name of the model
          dataset: a dataframe with observations to predict
          id_var: name of the variable id
          output: probs to get probability associated to each prediction, score to get the score
        """
        if id_var is not None:
            if id_var not in list(dataset):
                return "TEST DATA NOT SENT: variable '" + id_var + "' not found"

        # Prepare data for the request
        d = {}
        d['api_key'] = self.api_key
        d['model'] = model
        d['function'] = 'predict'
        d['data'] = []
        d['n_predictions'] = n_predictions
        answer = {}
        
        n = 0
        while n < dataset.shape[0]:
            if id_var is not None:
                new_obs = {'id':dataset[id_var][n]}
            else:
                new_obs = {'id':n}
            for i, name_var in enumerate(list(dataset)):
                if name_var not in [id_var]:
                    new_obs[name_var] = dataset[name_var][n]
                
            d['data'].append(new_obs)
            n += 1

        result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
        return json.loads(result.content)
    
    
    def analyze_predictions(self, model):
        """
        Input:
          model: name of the model
        """
        d = {}
        d['api_key'] = self.api_key
        d['function'] = 'analyze_predictions'
        d['model'] = model
        result = requests.get(self.api_url + '/TextClassifier', data=json.dumps(d))
        return json.loads(result.content)


import json, numpy as np

class InputOutput():
    def __init__(self, target_dir, json_name, var_dict=dict(), input_mat = None):  #var_dict is optional
        self.dir = target_dir
        self.name = json_name
        self.data = var_dict
        self.input_mat = input_mat
    
    
    def json_to_dict(self): # Used in the import of the target
        # Read JSON data from file
        with open(self.dir + self.name + '.json', 'r') as json_file:
            json_data = json_file.read()
        
        # Convert JSON data to dictionary
        data = json.loads(json_data)
        
        # Convert lists back to NumPy arrays in the dictionary
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = np.array(value)
        
        return data

    def dict_to_json(self): #Used in the export of the target
        # Convert ndarray to lists in the dictionary
        for key, value in self.data.items():
            if isinstance(value, np.ndarray):
                self.data[key] = value.tolist() #This makes the dictionary serializable to create a json. json.dumps needs list and not numpy arrays

        # Convert dictionary to JSON
        json_data = json.dumps(self.data, indent=4)

        # Write JSON data to a file
        with open(self.dir + self.name + '.json', 'w') as json_file:
            json_file.write(json_data)


        
        
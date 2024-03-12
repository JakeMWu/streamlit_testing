import numpy as np

def model_selector():
    """
    Allows a selection of model based on consent to using advanced population data, which may include protected information for better accuracy.

    User Inputs:
    Consent y/n
    Returns:
    best_performing_model or minimalistic_model (var): name of the chosen model
    """
    model_choice = input("Do you consent to using advanced population data, which may include protected information for better accuracy? (y/n) ").lower().strip()
    while True:
        if model_choice == 'y':
            return best_performing_model
        elif model_choice == 'n':
            return limited_model
        else:
            model_choice = input("Please, answer y/n. \nDo you consent to using advanced population data, which may include protected information for better accuracy? (y/n) ").lower().strip()
            
            
def get_data_from_user(model):
    """
    Gets needed data from user for model

    Args:
    model (var) : model to use to extract the relevant columns

    Returns:
    scaled_values (list): scaled values to implement in the model
    """
    # values empty list that will be filled with user input
    values = []
    for col in model['columns']:
        values.append([col, float(input(f'Provide a value for {col}: ').strip())])
      # for models with GDP, we calculate the log
        if col == 'GDP':
            values[-1][1] = np.log(values[-1][1])
    # scaling the data (MinMaxScaler transformation)
    scaled_values = scale(values, scaler)
    return scaled_values

def scale(values, scaler):
    """
    Scales list of values using MinMaxScaler transformation

    Args:
    values (list) : tuples in the form (column, input value)
    scaler (dic)  : Dictionary with columns as keys and dictionaries of mins and maxes as values

    Returns:
    scaled_list (list): scaled list of input values
    """
    scaled_list = []
    for col, value in values:
        X_std = (value - scaler[col]['min']) / (scaler[col]['max'] - scaler[col]['min'])
        #    X_scaled = X_std * (1 - 0) + 0 #default max is 1, min is 0. It's usually * (max - min) + min
        scaled_list.append(X_std)
    return scaled_list

def life_expectancy_predictor(model, scaled_values):
    """
    Performs Life Expectancy prediction using a specificed model with the data provided by the user.

    Args:
    model (dic) : model to use for the prediction
    scaled_values (list) : scaled values to use for the prediction

    Returns:
    life_expectancy_prediction (float) : predicted life expectancy

    """
    # initialising life_expectancy_prediction with the constant value
    life_expectancy_prediction = model['params'][0]
    # implementing the model
    for p, x in zip(model['params'][1:], scaled_values):
        life_expectancy_prediction += p*x
    # print statement with the final life expectancy prediction
    if 40.639251 < life_expectancy_prediction < 97.072899:  # Predition within 3 standard deviation from the mean
        print('The estimated Life Expectancy is ', round(life_expectancy_prediction, 2))
    else:
        # Life Expectancy out of expected ranges
        print('\nWarning: The estimated Life Expectancy is far out the expected range.\n')
        # Negative Life Expectancy retuns 0
        if life_expectancy_prediction < 0:
            life_expectancy_prediction = 0
            print('The estimated Life Expectancy is ', round(life_expectancy_prediction, 2))
    # returns life_expectancy_prediction value (float) in case it is wanted for futher use
    return life_expectancy_prediction

def main ():
    model = model_selector()
    scaled_values = get_data_from_user(model)
    life_expectancy_predictor(model, scaled_values)
    
# DATA
best_performing_model = {'columns':['Adult Mortality', 'Infant Deaths', 'GDP'], 'params' : [76.6453, -30.258006, -17.446125, 4.720947]}
limited_model = {'columns':['Adult Mortality', 'GDP'], 'params' : [71.265829, -40.091971, 12.347190]}
scaler = {'GDP': {'max': 11.629979 , 'min': 4.997212}, 'Adult Mortality': {'max': 703.677, 'min': 49.384}, 'Year': {'max': 2015, 'min': 2000},'Infant Deaths': {'max': 135.6, 'min': 1.8}}
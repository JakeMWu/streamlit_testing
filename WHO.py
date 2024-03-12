import streamlit as st
import numpy as np

def scale(value, col):
    X_std = (value - scaler[col]['min']) / (scaler[col]['max'] - scaler[col]['min'])
    return X_std

def life_expectancy_predictor(model, scaled_values):
    life_expectancy_prediction = model['params'][0]
    for p, x in zip(model['params'][1:], scaled_values):
        life_expectancy_prediction += p * x
    if 40.639251 < life_expectancy_prediction < 97.072899:
        st.write(f'The estimated Life Expectancy is {round(life_expectancy_prediction, 2)} years')
    else:
        st.write('\nWarning: The estimated Life Expectancy is far out the expected range.\n')
        if life_expectancy_prediction < 0:
            life_expectancy_prediction = 0
            st.write('The estimated Life Expectancy is ', round(life_expectancy_prediction, 2))
    return life_expectancy_prediction

def main():
    st.title('Life Expectancy Predictor')

    if 'model' not in st.session_state:
        st.session_state['model'] = None
    
    consent = st.radio(
        "Do you consent to using advanced population data, which may include protected information for better accuracy?",
        ('Yes', 'No'), key='consent'
    )

    if consent == 'Yes':
        st.session_state['model'] = best_performing_model
    else:
        st.session_state['model'] = limited_model

    if st.session_state['model']:
        values = []
        for col in st.session_state['model']['columns']:
            value = st.number_input(f'Provide a value for {col}:', key=col, format="%f")
            if col == 'GDP':
                value = np.log(value)
            values.append(scale(value, col))
        
        if st.button('Predict Life Expectancy'):
            life_expectancy_predictor(st.session_state['model'], values)

if __name__ == "__main__":
    best_performing_model = {'columns': ['Adult Mortality', 'Infant Deaths', 'GDP'], 'params': [76.6453, -30.258006, -17.446125, 4.720947]}
    limited_model = {'columns': ['Adult Mortality', 'GDP'], 'params': [71.265829, -40.091971, 12.347190]}
    scaler = {'GDP': {'max': 11.629979, 'min': 4.997212}, 'Adult Mortality': {'max': 703.677, 'min': 49.384}, 'Infant Deaths': {'max': 135.6, 'min': 1.8}}

    main()
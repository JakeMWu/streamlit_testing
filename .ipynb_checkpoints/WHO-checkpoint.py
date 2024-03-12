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
        years = int(life_expectancy_prediction)  # This will get the whole number part (years)
        days = int((life_expectancy_prediction - years) * 365)  # Calculate the days from the remainder
        st.write(f'The estimated Life Expectancy is {years} years and {days} days')
    else:
        st.write('\nWarning: The estimated Life Expectancy is far out the expected range.\n')
        if life_expectancy_prediction < 0:
            life_expectancy_prediction = 0
            
            st.write('The estimated Life Expectancy is ', round(life_expectancy_prediction, 2))
    return life_expectancy_prediction

def main():
    st.image("https://www.un.org/youthenvoy/wp-content/uploads/2014/09/WHO.jpg", use_column_width=True)
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
        # Specify the unit for each column
        units = {'GDP': 'per capita', 'Adult Mortality': 'per 1000', 'Infant Deaths': 'per 1000'}
        for col in st.session_state['model']['columns']:
            # Include the unit in the prompt
            prompt = f'Provide a value for {col} ({units.get(col, "")}):'
            value = st.number_input(prompt, key=col, format="%f")
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
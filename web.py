import streamlit as st
import pandas as pd
import pickle
import json

import json

def load_locations():
    with open("columns.json", "r") as f:
        data = json.load(f)

    locations = data["data_columns"][3:]
    return locations


def load_model(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def get_estimated_price(total_sqft, bhk, bathrooms, location, locations, model):
    location_index = locations.index(location)

    features = [total_sqft, bhk, bathrooms] + [0] * len(locations)
    features[location_index + 3] = 1

    estimated_price = model.predict([features])[0]
    return estimated_price



def main():
    st.title('HomePriceXpert - Bangalore Home Price Estimator')
    st.markdown('Estimate the price of a home in Bangalore')

    total_sqft = st.number_input('Area (Square Feet)', value=1000)
    bhk = st.radio('BHK', [1, 2, 3, 4, 5], index=1)
    bathrooms = st.radio('Bath', [1, 2, 3, 4, 5], index=1)

    locations = load_locations()
    location = st.selectbox('Location', ['Choose a Location'] + locations)

    model = load_model("bangalore_home_prices_model.pickle")

    if st.button('Estimate Price'):
        if location != 'Choose a Location':
            estimated_price = get_estimated_price(total_sqft, bhk, bathrooms, location, locations, model)
            st.success(f'Estimated Price: {estimated_price:.2f} Lakh')
        else:
            st.error('Please select a valid location.')


if __name__ == '__main__':
    main()


import pickle 
import streamlit as st
import pandas as pd
import os

model_path = os.path.join(os.path.dirname(__file__), 'car_price_predictor.pkl')
model = pickle.load(open(model_path, 'rb'))

def main():
    st.title('Car Pricing Predictor')

    # Define car brands and their corresponding models
    car_data = {
        'Ambassador': ['Grand', 'Classic'],
        'Chevrolet': ['Spark', 'Aveo', 'Sail', 'Cruze', 'Optra', 'Beat'],
        'Daewoo': ['Matiz'],
        'Datsun': ['GO', 'RediGO'],
        'Fiat': ['Linea', 'Grande Punto', 'Punto', 'Avventura'],
        'Ford': ['Freestyle', 'Fusion', 'EcoSport', 'Ikon', 'Aspire', 'Classic', 'Figo', 'Fiesta'],
        'Honda': ['Civic', 'Amaze', 'City', 'Jazz', 'WR-V', 'Brio'],
        'Hyundai': ['i20', 'i10', 'Elantra', 'Getz', 'Venue', 'EON', 'Accent', 'Verna', 'Grand i10', 'Xcent', 'Creta', 'Sonata', 'Santro', 'Elite'],
        'Kia': ['Seltos'],
        'Mahindra': ['Logan', 'KUV 100', 'XUV300', 'Verito'],
        'Mahindra Renault': ['Logan'],
        'Maruti': ['A-Star', 'Omni', 'Eeco', '800', 'Ciaz', 'S-Presso', 'Baleno', 'Alto', 'Esteem', 'S-Cross', 'Wagon R', 'Ignis', 'Zen', 'Vitara Brezza', 'Swift', 'SX4', 'Celerio', 'Ritz', 'Dzire'],
        'Mercedes-Benz': ['B Class'],
        'Mitsubishi': ['Lancer'],
        'Nissan': ['Micra', 'Kicks', 'Sunny', 'Terrano'],
        'Opel': ['Astra'],
        'Renault': ['KWID', 'Fluence', 'Koleos', 'Duster', 'Pulse', 'Captur', 'Scala'],
        'Skoda': ['Laura', 'Octavia', 'Rapid', 'Superb', 'Fabia'],
        'Tata': ['Bolt', 'Tiago', 'Nexon', 'Zest', 'Tigor', 'Manza', 'Indigo', 'Indica'],
        'Toyota': ['Glanza', 'Platinum Etios', 'Yaris', 'Etios', 'Corolla'],
        'Volkswagen': ['Jetta', 'Ameo', 'CrossPolo', 'Passat', 'Polo', 'Vento'],
        'Volvo': ['V40']
    }

    # Brand selection
    brand = st.selectbox('Select Car Brand', list(car_data.keys()))

    # Model selection based on the selected brand
    model_options = car_data.get(brand, [])
    selected_model = st.selectbox('Select Car Model', model_options)

    Fuel = st.selectbox('Select Fuel Type', ['Diesel','Petrol','CNG','LPG'])

    Seller = st.selectbox('Select Type of Seller', ['Individual', 'Dealer','Trustmark Dealer'])
    
    Transmission = st.selectbox('Select Car Transmission', ['Manual', 'Automatic'])
    
    Owner = st.selectbox('Select Present Car Owner Type', ['First Owner','Second Owner','Third Owner','Fourth & Above Owner'])

    # Input fields for other variables without immediate validation
    Year = st.text_input('Year')
    Km_driven = st.text_input('Km driven')
    engine = st.text_input('Engine')
    max_power = st.text_input('Max Power')
    mileage_kmpl = st.text_input('Mileage (kmpl)')

    if st.button('Predict'):
        # Function to validate numeric input during prediction
        def validate_numeric_input(input_value, field_name):
            try:
                return float(input_value)
            except ValueError:
                st.error(f"Invalid input for {field_name}. Please enter a numeric value.")
                return None

        # Validate inputs on 'Predict' click
        Year = validate_numeric_input(Year, 'Year')
        Km_driven = validate_numeric_input(Km_driven, 'Km driven')
        engine = validate_numeric_input(engine, 'Engine')
        max_power = validate_numeric_input(max_power, 'Max Power')
        mileage_kmpl = validate_numeric_input(mileage_kmpl, 'Mileage (kmpl)')

        # Check if all inputs are valid before proceeding
        if None not in [Year, Km_driven, engine, max_power, mileage_kmpl]:
            try:
                input_data = pd.DataFrame([{
                    'year': Year,
                    'km_driven': Km_driven,
                    'fuel': Fuel,
                    'seller_type': Seller,
                    'transmission': Transmission,
                    'owner': Owner,
                    'engine': engine,
                    'max_power': max_power,
                    'brand': brand,
                    'model': selected_model,
                    'mileage_kmpl': mileage_kmpl
                }])

                # Predict the price using the pipeline model
                prediction = model.predict(input_data)
                output = round(prediction[0] * 19.61, -3)
                formatted_output = "{:,.0f}".format(output)
                st.success(f'You Can Sell Your Car for {formatted_output} Naira')
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")

if __name__ == '__main__':
    main()

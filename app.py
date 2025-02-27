import streamlit as st
import requests
import openai
from datetime import datetime

def get_weather_data(city,weather_api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get (complete_url)
    return response. json()

#Function to generate a weather description using OpenAI's GPT model odef generate weather description data openai apinkey:
def generate_weather_description (data, openai_api_key):
    openai.api_key = openai_api_key 
    
    try:
        #Convert temperature from Kelvin to Celsius
        temperature = data[ 'main']['temp'] - 273.15 # Convert Kelvin to Celsius
        description = data[ 'weather'][0][ 'description']
        prompt = f"The current weather in your city is {description} with a temperature of {temperature: 1f}*C. Explain this in a simple way for our general audience"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains weather in a simple way."},
                {"role": "user", "content": prompt},
            ], 
            max_tokens=60
        )
        return response['choices'][0]['message']['content'].strip()
    
    except Exception as e:
        return str(e)
        
def get_weekly_forecast(weather_api_key, lat, lon) :
    base_url = "https://api.openweathermap.org/data/2.5/"
    complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get (complete_url)
    return response.json()

def display_weekly_forecast (data) :
    try:
        st.write("============================================")
        st.write("### Weekly Weather Forecast")
        displayed_dates = set()     # To keep track of dates for which forecast has been displayed
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("", "Day")
        
        with c2:
            st.metric("", "Desd" )
        
        with c3:
            st.metric("", "Min_temp")
        
        with c4:
            st.metric("", "Max_temp")
        
        for day in data['list']:
            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
            # Check if the date has already been displayed
            if date not in displayed_dates:
                displayed_dates.add(date)
                min_temp = day['main']['temp_min'] - 273.15 # Convert Kelvin to Celsius
                max_temp = day['main']['temp_max'] - 273.15
                description = day['weather'][0]['description' ]
                with c1:
                    st.write(f" {date}")
                with c2:
                    st.write(f" {description.capitalize()}")
                with c3:
                    st.write(f" {min_temp:.1f}°C")
                with c4:
                    st.write(f" {max_temp: .1f}°C")
    except Exception as e:
        st.error("Error in displaying weekly forecast: " + str(e))
        
        
def main():
    st.sidebar.title("Weather Forecasting with LLM")
    city = st. sidebar.text_input("Enter city name", "London")
    
    # API keys
    weather_api_key = "fcf7799b55f7dfb933edbad52a49b741" # Replace with your OpenWeatherMap API key
    openai_api_key = "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"

    # Button to fetch and display weather data
    submit = st.sidebar.button("Get Weather")
    
    if submit:
        st.title("Weather Updates for " + city + " is:") 
        with st. spinner('Fetching weather data...'):
            weather_data = get_weather_data(city, weather_api_key)
            print(weather_data)
            
            if weather_data.get("cod") != 404:
                col1, col2 = st.columns(2)
                with col1:
                    st. metric("Temperature ", f"{weather_data[ 'main' ]['temp'] - 273.15: .2f} °C")
                    st.metric("Humidity ", f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric("Pressure ", f"{weather_data['main']['pressure']} hPa")
                    st.metric("Wind Speed ", f"{weather_data['wind'] ['speed']} m/s")
                    
                lat = weather_data['coord']['lat']
                lon = weather_data['coord'] ['lon']
                
                # Generate and display a friendly weather description
                weather_description = generate_weather_description (weather_data, openai_api_key)
                st.write(weather_description)
                
                #Call function to get weekly forecast
                forecast_data = get_weekly_forecast(weather_api_key, lat, lon)
                print(forecast_data)
                if forecast_data.get ("cod") != "404":
                    display_weekly_forecast(forecast_data)
                    
            else:
                # Display an error message if the city is not found
                st.error("City not found or an error occurred!")

if __name__ == "__main__":
    main()
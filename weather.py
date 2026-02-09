from tkinter import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests
import pytz

root = Tk()
root.title("weather App")
root.geometry("900x500+300+200")
root.resizable(False,False)

def getWeather():
    
    try:
        city=textfield.get()
        
        if not city:
            messagebox.showerror("weather App","Please enter a city name!")
            return

        #weather - Using Open-Meteo API (free, no auth needed)
        geo_api=f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response=requests.get(geo_api).json()
        
        if not geo_response.get('results'):
            messagebox.showerror("weather App","City not found!")
            return
        
        geo_data=geo_response['results'][0]
        latitude=geo_data['latitude']
        longitude=geo_data['longitude']
        timezone=geo_data.get('timezone', 'UTC')
        
        # Get current time in that timezone
        try:
            tz=pytz.timezone(timezone)
            local_time=datetime.now(tz)
            current_time=local_time.strftime("%I:%M %p")
            clock.config(text=current_time)
        except:
            clock.config(text="--:-- --")
        
        name.config(text="CURRENT WEATHER")
        
        weather_api=f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl&timezone=auto"
        weather_response=requests.get(weather_api).json()
        
        print(f"API Response: {weather_response}")
        
        if 'current' not in weather_response:
            print(f"Available keys: {weather_response.keys()}")
            messagebox.showerror("weather App","Could not fetch weather data")
            return
        
        current=weather_response['current']
        temp=int(current['temperature_2m'])
        
        # Convert weather code to description
        weather_code=current.get('weather_code', 0)
        weather_descriptions={
            0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",45:"Foggy",48:"Foggy",
            51:"Light drizzle",53:"Moderate drizzle",55:"Dense drizzle",61:"Slight rain",63:"Moderate rain",
            65:"Heavy rain",71:"Slight snow",73:"Moderate snow",75:"Heavy snow",77:"Snow grains",
            80:"Slight rain showers",81:"Moderate rain showers",82:"Violent rain showers",85:"Slight snow showers",86:"Heavy snow showers",
            95:"Thunderstorm",96:"Thunderstorm with hail",99:"Thunderstorm with hail"
        }
        condition=weather_descriptions.get(weather_code,"Unknown")
        description=condition
        humidity=current['relative_humidity_2m']
        wind=current['wind_speed_10m']
        pressure=int(current['pressure_msl'])

        t.config(text=f"{temp}°C")
        c.config(text=f"{condition} | FEELS LIKE {temp}°C")

        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("weather App",f"Error: {str(e)}")


#search box
Search_image=PhotoImage(file=r"C:\Users\KIIT0001\Downloads\search.png.png")
myimage=Label(image=Search_image)
myimage.place(x=20,y=20)

textfield=tk.Entry(root,justify='center',width=17,font=('poppins',25,'bold'),bg='#404040',border=0,fg='white')
textfield.place(x=50,y=40)
textfield.focus()

search_icon=PhotoImage(file=r"C:\Users\KIIT0001\Downloads\Copy of search_icon.png")
myimage_icon=Button(image=search_icon,borderwidth=0,cursor='hand2',bg="#404040",command=getWeather)
myimage_icon.place(x=400,y=34)

#logo
Logo_image=PhotoImage(file=r"C:\Users\KIIT0001\Downloads\Copy of logo.png")
logo=Label(image=Logo_image)
logo.place(x=150,y=100)

#bottom box
Frame_image=PhotoImage(file=r"C:\Users\KIIT0001\Downloads\Copy of box.png")
frame=Label(image=Frame_image)
frame.pack(padx=5,pady=5,side=BOTTOM)

#time
name=Label(root,font=('arial',15,'bold'))
name.place(x=30,y=100)
clock=Label(root,font=('arial',20))
clock.place(x=30,y=130)

#labels
label1=Label(root,text='WIND',font=('arial',15,'bold'),fg='white',bg='#1ab5ef')
label1.place(x=120,y=400)

label2=Label(root,text='HUMIDITY',font=('arial',15,'bold'),fg='white',bg='#1ab5ef')
label2.place(x=250,y=400)

label3=Label(root,text='DESCRIPTION',font=('arial',15,'bold'),fg='white',bg='#1ab5ef')
label3.place(x=430,y=400)

label4=Label(root,text='PRESSURE',font=('arial',15,'bold'),fg='white',bg='#1ab5ef')
label4.place(x=650,y=400)

t=Label(font=('arial',70,'bold'),fg='#ee666d')
t.place(x=400,y=150)
c=Label(font=('arial',15,'bold'),fg='#1ab5ef')
c.place(x=400,y=250)

w=Label(text='...',font=('arial',20,'bold'),bg='#1ab5ef')
w.place(x=120,y=430)

h=Label(text='...',font=('arial',20,'bold'),bg='#1ab5ef')
h.place(x=280,y=430)

d=Label(text='...',font=('arial',20,'bold'),bg='#1ab5ef')
d.place(x=450,y=430)

p=Label(text='...',font=('arial',20,'bold'),bg='#1ab5ef')
p.place(x=670,y=430)

root.mainloop()
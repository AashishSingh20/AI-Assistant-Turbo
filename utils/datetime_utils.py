import datetime
from speech import speak

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    print(current_time)
    speak(f"The time is {current_time}")

def tell_date():
    current_date = datetime.datetime.now().strftime("%d %B %Y")
    print(current_date)
    speak(f"Today's date is {current_date}")
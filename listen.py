 import sounddevice as sd
import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Constants
DURATION = 5  # seconds
SAMPLE_RATE = 16000
LED_PIN = 17  # GPIO pin for the LED

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(LED_PIN, GPIO.OUT)  # Set LED pin as output

def recognize_speech(audio_data):
    recognizer = sr.Recognizer()
    try:
        audio = sr.AudioData(audio_data.tobytes(), SAMPLE_RATE, 2)
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()  # Convert command to lowercase for easier matching
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def listen():
    print("Listening for command...")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    return audio_data

def control_led(command):
    if "turn the led on" in command:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        print("LED is ON")
    elif "turn the led off" in command:
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        print("LED is OFF")
    else:
        print("No valid command received")

if __name__ == "__main__":
    try:
        while True:
            audio_data = listen()
            command = recognize_speech(audio_data)
            if command:
                control_led(command)
            time.sleep(1)  # Optional: add a delay before listening again
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings on exit

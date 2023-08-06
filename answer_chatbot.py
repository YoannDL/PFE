import qi
import speech_recognition as sr
import openai
import pyttsx3

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Set up OpenAI API
openai.api_key = "api_key"  # Replace with your OpenAI API key

# Chatbot interaction function
def chat_with_bot(user_input):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=user_input,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Nao robot connection function
def connect_to_nao(robot_ip):
    try:
        session = qi.Session()
        session.connect("tcp://" + robot_ip + ":9559")
        return session
    except Exception as e:
        print("Error connecting to Nao:", str(e))
        return None

# Nao robot speech recognition function
def speech_to_text(session):
    try:
        memory = session.service("ALMemory")
        asr = session.service("ALSpeechRecognition")
        asr.setLanguage("English")
        asr.subscribe("BiodiversityBot")

        while True:
            word_recognized = memory.getData("WordRecognized")
            if word_recognized and word_recognized[0] == "exit":
                asr.unsubscribe("BiodiversityBot")
                return None

            if word_recognized and len(word_recognized[1]) > 0:
                user_input = word_recognized[1][0]
                return user_input

    except Exception as e:
        print("Error with speech recognition:", str(e))
        return None

# Nao robot text to speech function
def text_to_speech(session, text):
    try:
        tts = session.service("ALTextToSpeech")
        tts.setParameter("speed", 100)  # Adjust the speech speed if needed
        tts.say(text)

    except Exception as e:
        print("Error with text-to-speech:", str(e))

# Main function for Nao robot interaction
def main(robot_ip):
    session = connect_to_nao(robot_ip)
    if not session:
        print("Could not connect to Nao robot.")
        return

    print("BiodiversityBot: Hello! I'm Nao, a chatbot created by Yoann here to answer your questions about biodiversity and sustainable development. You can ask me anything you want. Say 'exit' to end the conversation.")

    while True:
        print("Listening...")
        user_input = speech_to_text(session)

        if user_input:
            print("You:", user_input)

            if user_input.lower() == "exit":
                break

            # Chat with the bot
            bot_response = chat_with_bot(user_input)
            print("BiodiversityBot:", bot_response)

            # Convert chatbot response to speech and play on Nao robot's speaker
            text_to_speech(session, bot_response)

if __name__ == "__main__":
    robot_ip = "YOUR_NAO_ROBOT_IP"  # Replace with your Nao robot's IP address
    main(robot_ip)

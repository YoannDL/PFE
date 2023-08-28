# set the environment variable OPENAI_API_KEY with your actual API key before running the script. You can do this in your shell before running the Python script: export OPENAI_API_KEY=your-openai-api-key-here
import openai
import speech_recognition as sr
from naoqi import ALProxy
import string
import os  # For reading environment variables

#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

tts = ALProxy("ALTextToSpeech", "your_NAO_IP", 9559)
motion = ALProxy("ALMotion", "your_NAO_IP", 9559)

# Securely fetch OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

educational_frames = [
    {"speech": "Let's talk about trees.", "gesture": "Wave"},
    {"speech": "Trees help us breathe.", "gesture": "Breathe"},
    {"speech": "Did you know a single tree can absorb as much as 48 pounds of carbon dioxide per year?", "gesture": "Point"},
    {"speech": "This is important because carbon dioxide is a greenhouse gas.", "gesture": "Clap"},
    {"speech": "Moving on to water.", "gesture": "Wave"},
    {"speech": "Water is the essence of life.", "gesture": "Breathe"},
    {"speech": "Unfortunately, our oceans are filled with plastic.", "gesture": "ThumbsUp"},
    {"speech": "It takes hundreds of years for plastic to decompose.", "gesture": "Clap"},
    {"speech": "Let's discuss animals.", "gesture": "Wave"},
    {"speech": "Many species are endangered due to habitat loss.", "gesture": "Breathe"},
    {"speech": "Saving them is crucial for biodiversity.", "gesture": "Point"},
    {"speech": "Biodiversity is important for a balanced ecosystem.", "gesture": "Clap"},
    {"speech": "Lastly, let's talk about energy.", "gesture": "Wave"},
    {"speech": "Solar and wind energy are renewable.", "gesture": "Breathe"},
    {"speech": "They don't emit greenhouse gases.", "gesture": "ThumbsUp"},
    {"speech": "Switching to renewable energy can help combat climate change.", "gesture": "Clap"},
    {"speech": "Remember, every little action counts.", "gesture": "Point"},
    {"speech": "So, let's all make a pledge to take better care of our planet!", "gesture": "Breathe"}
]

def process_question(raw_question):
    # Trim leading and trailing white spaces
    cleaned_question = raw_question.strip()
    
    # Convert to lowercase for uniformity (optional)
    cleaned_question = cleaned_question.lower()
    
    # Remove punctuations (optional)
    cleaned_question = ''.join(char for char in cleaned_question if char not in string.punctuation)
    
    return cleaned_question

def enact_frame(frame):
    speech = frame["speech"]
    gesture = frame["gesture"]
    
    # Use NAO SDK to speak
    tts.say(speech)
    
    # Use the handle_gesture function to make gestures
    handle_gesture(gesture)
    
    # Use NAO SDK to make gestures
    if gesture == "Wave":
        motion.openHand("LHand")
        motion.closeHand("LHand")
    elif gesture == "Breathing":
        # Get the robot to an initial neutral standing pose
        motion.stiffnessInterpolation("Body", 1.0, 1.0)
        motion.moveTo(0.0, 0.0, 0.0)
        motion.waitUntilMoveIsFinished()

        # Perform the "inhale" part of the breathing
        # Raising the arms to simulate inhale
        motion.angleInterpolation(
            ["LShoulderPitch", "RShoulderPitch"],
            [-0.5, -0.5],
            [1, 1],
            isAbsolute=True,
        )

        # Perform the "exhale" part of the breathing
        # Lowering the arms to simulate exhale
        motion.angleInterpolation(
            ["LShoulderPitch", "RShoulderPitch"],
            [1.5, 1.5],
            [1, 1],
            isAbsolute=True,
        )

        # Return to a neutral standing pose
        motion.moveTo(0.0, 0.0, 0.0)
        motion.waitUntilMoveIsFinished()
        motion.stiffnessInterpolation("Body", 0.0, 1.0)

def get_childrens_question():
    try:
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source)

        return recognizer.recognize_google(audio_data)
    except Exception as e:
        print(f"An error occurred while capturing audio: {e}")
        tts.say("I encountered an error while capturing audio. Please try again.")
        return None

def fetch_gpt3_response_and_gesture(question, engine="davinci"):
    try:
        prompt = f"Question: {question}\nAnswer:"
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=50
        )
        
        answer = response.choices[0].text.strip()
        
        # Now, generate a directive for NAO's gestures
        gesture_prompt = f"Based on the context of the question '{question}', what gesture should NAO robot make?\nGesture:"
        gesture_response = openai.Completion.create(
            engine=engine,
            prompt=gesture_prompt,
            max_tokens=20
        )
        
        gesture = gesture_response.choices[0].text.strip()
        return answer, gesture
    except Exception as e:
        print(f"An error occurred: {e}")
        tts.say("I encountered an error while generating a response. Please try again.")
        return "I couldn't fetch an answer due to an error.", "None"

def handle_gesture(gesture_directive):
    if gesture_directive == "Wave":
        # Open and close the left hand to wave
        motion.openHand("LHand")
        motion.closeHand("LHand")

    elif gesture_directive == "ThumbsUp":
        # Raise the left arm and open the hand
        motion.setAngles("LShoulderRoll", -0.2, 0.2)
        motion.setAngles("LWristYaw", 1.5, 0.2)
        motion.openHand("LHand")
        # Close all fingers except the thumb
        motion.setAngles("LHand", 0.6, 0.2)

    elif gesture_directive == "Clap":
        # Open both hands and move them to the clapping position
        motion.openHand("LHand")
        motion.openHand("RHand")
        motion.setAngles(["LShoulderRoll", "RShoulderRoll"], [-0.2, 0.2], [0.2, 0.2])
        # Close both hands to clap
        motion.closeHand("LHand")
        motion.closeHand("RHand")

    elif gesture_directive == "Point":
        # Point using the right hand index finger
        motion.openHand("RHand")
        motion.setAngles(["RWristYaw", "RShoulderRoll"], [1.5, 0.2], [0.2, 0.2])
        motion.setAngles("RHand", 0.6, 0.2)  # Close all fingers except the index finger

    # Add more gestures as needed

def conduct_quiz():
    try:
        # Generate a quiz question
        quiz_prompt = "Generate a multiple-choice question about biodiversity."
        quiz_question = fetch_gpt3_response_and_gesture(quiz_prompt)

        # Speak the quiz question and options
        tts.say(quiz_question)

        # Get the children's answer
        child_answer = get_childrens_question()

        # Validate the answer using GPT-3
        validation_prompt = f"Is the answer '{child_answer}' correct for the quiz question: {quiz_question}"
        is_correct = fetch_gpt3_response_and_gesture(validation_prompt)

        # Let NAO speak whether the answer was correct or not
        tts.say(is_correct)
    except Exception as e:
        print(f"An error occurred while conducting the quiz: {e}")
        tts.say("I encountered an error while conducting the quiz. Let's try again later.")
        return "Quiz Error", "None"

# Conclusion
tts.say("Let's all pledge to be friends of the Earth! Repeat after me: I promise to take care of our planet.")

for frame in educational_frames:
    enact_frame(frame)
    
    raw_question = get_childrens_question()

    if raw_question is not None:    
        # Process the question
        processed_question = process_question(raw_question)
        
        # Fetch GPT-3 generated answer and gesture
        gpt3_answer, gpt3_gesture = fetch_gpt3_response_and_gesture(processed_question)
        
        # Let NAO enact the gesture
        handle_gesture(gpt3_gesture)
        
        # Let NAO speak the answer
        tts.say(gpt3_answer)
    else:
        tts.say("Sorry, I was unable to capture the question. Could you please repeat it?")

    # Fetch children's question
    raw_question = get_childrens_question()

    # Process the question
    processed_question = process_question(raw_question)

    # Fetch GPT-3 generated answer and gesture
    gpt3_answer, gpt3_gesture = fetch_gpt3_response_and_gesture(processed_question)

    # Let NAO enact the gesture
    handle_gesture(gpt3_gesture)

    # Let NAO speak the answer
    tts.say(gpt3_answer)


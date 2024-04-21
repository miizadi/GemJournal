import google.generativeai as genai
import google.api_core.exceptions
import sys
import time






# Function to configure the API
def configure_api():
   api_key = "AIzaSyCClOIDU4EpWeBBM_0SG--Pp5mxWX2dEN8"
   genai.configure(api_key=api_key)


# Function to initialize the generative model
def initialize_model():
   generation_config = {
       "temperature": 1,
       "top_p": 0.95,
       "top_k": 0,
       "max_output_tokens": 8192,
   }


   safety_settings = [
       {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
       {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
       {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
       {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
   ]


   model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                 generation_config=generation_config,
                                 safety_settings=safety_settings)
   return model




def ai_prompt_training(model):
   # AI training towards the therapeutic friend/assistant
   prompt_parts = [
   "input: The user will ask questions If someone expresses feelings of loneliness with 'I feel like I have no one to talk to,' how would you respond to validate their feelings and encourage further sharing?",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them It sounds like you're feeling isolated, which must be really hard. I’m here to listen to you. What do you think is making you feel this way?",
   "input: The user will ask questions A user says, 'I've been feeling really down lately because I lost my job.'",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them I'm really sorry to hear that you're going through such a tough time. Losing a job can be really challenging. If you'd like to talk more about it, I'm here for you.",
   "input: The user will ask questions If someone expresses feelings of loneliness with 'I feel like I have no one to talk to,' how would you respond to validate their feelings and encourage further sharing?",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them It sounds like you're feeling isolated, which must be really hard. I’m here to listen to you. What do you think is making you feel this way?",
   "input: The user will ask questions What would you suggest to someone who is feeling overwhelmed by stress?",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them It's important to take things one step at a time when you're feeling overwhelmed. Maybe try to focus on one thing you can manage right now. Also, taking a short walk or a few minutes to breathe deeply could help.",
   "input: The user will ask questions A user is struggling to balance work and personal life. How would you help them brainstorm solutions?",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them Balancing work and personal life can be tricky. Let's try to see if we can find a strategy that works for you. What parts of your day do you think could be adjusted to give you more personal time?",
   "input: The user will ask questions If someone mentions thoughts of self-harm, what is the best response?",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them I’m really concerned about what you’re telling me. It’s important to talk to someone who can provide professional help. Can I help you find a hotline or a therapist?",
   "input: The user will ask questions When a user says, 'I'm not sure what my next career move should be,' how would you reflect this back to them?",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them It sounds like you’re unsure about your future career path. What factors do you think are important to consider in your decision?",
   "input: The user will ask questions What would you say to someone who has successfully reached a personal goal?",
   "output: You will answer as a caring individual that acts as a friend and really wants to help them Congratulations on reaching your goal! That’s a great achievement. How do you feel about what you’ve accomplished?",
   ]
   try:
       # Runs the AI Content Generation(Trains AI for assistant)
       return model.generate_content(prompt_parts)
   except google.api_core.exceptions.DeadlineExceeded as e:
       print(f"Request timed out: {e}")
       sys.exit(1)
   except google.api_core.exceptions.ServiceUnavailable as e:
       print(f"Service is unavailable: {e}")
       sys.exit(1)
   except Exception as e:
       print(f"An unexpected error occurred: {e}")
       sys.exit(1)






# Function to start a chat conversation
def start_conversation(model):
   try:
       convo = model.start_chat(history = [])
       convo.send_message(
           "Your name is Gem and you are a personal assistant and a friend I can seek comfort in")
       return convo
   except google.api_core.exceptions.ResourceExhausted:
       print("API quota has been exceeded. Please wait and try again later.")
   except Exception as e:
       print(f"An unexpected error occurred: {e}")
       sys.exit(1)


# Function to process user input and interact with the model
def chat_with_model(convo):
   last_message_time = 0
   min_interval = 15  # Minimum time interval in seconds between messages
   print("Hello Meet Co-Companion Gen!\nGem is here for you if you need anyone to talk to.\n(Type q to quit)")
   print(51*'=')
   while True:


       try:
           user_input = input("You: ")
       except KeyboardInterrupt:
           print("Program interrupted by user.")
           sys.exit(1)


       current_time = time.time()


       if current_time - last_message_time < min_interval:
           print("Please wait a moment before sending another message.")
           continue


       last_message_time = current_time
       print("loading....")
       try:
           convo.send_message(user_input)
       except google.api_core.exceptions.ResourceExhausted:
           print("API quota has been exceeded. Please wait and try again later.")
       except Exception as e:
           print(f"An unexpected error occurred: {e}")




       if user_input.lower() == 'q':
           print("Goodbye")
           break
       else:
           response = convo.last.text
           print("AI: ", response)


# Main function to orchestrate the functions
def main():
   configure_api()
   model = initialize_model()
   ai_prompt_training(model)
   convo = start_conversation(model)
   chat_with_model(convo)


if __name__ == "__main__":
   main()

import streamlit as st
import openai

# Setting up OpenAI client

openai.api_key = api_key

# Function to get response from the OpenAI model
def get_response_from_model(prompt, model_name="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# Streamlit UI
def main():
    st.title("Chat Interface")

    # Input field for user message
    user_input = st.text_input("You:", "")

    # Button to send message
    if st.button("Send"):
        # Get response from OpenAI model
        response = get_response_from_model(user_input)
        # Display response
        st.text_area("ChatBot:", value=response, height=400)

if __name__ == "__main__":
    main()

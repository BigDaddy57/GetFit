from django.shortcuts import render
import requests
from django.http import JsonResponse

def chatbot_view(request):
    # Get the user input from the request
    user_input = request.GET.get('input', '')
    
    # Make a request to the ChatGPT API
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    }
    data = {
        'messages': [{'role': 'system', 'content': 'You are a user'}, {'role': 'user', 'content': user_input}]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    response_data = response.json()
    
    # Extract the chatbot's reply from the response
    chatbot_reply = response_data['choices'][0]['message']['content']
    
    # Return the chatbot's reply as a JSON response
    return JsonResponse({'reply': chatbot_reply})


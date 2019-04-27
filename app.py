import os
from pymessenger.bot import Bot
from chalice import Chalice, Response

# Reading environment variables
VERIFY_TOKEN = os.getenv('FB_VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')

app = Chalice(app_name='facebook-messenger-serverless')
bot = Bot(ACCESS_TOKEN)

@app.route('/fbevent', methods=['POST', 'GET'])
def fbevent():

    query_params = app.current_request.query_params

    # Assert verify token and respond to challenge
    if app.current_request.method == 'GET':

        challenge = query_params['hub.challenge']
        received_verify_token = query_params['hub.verify_token']

        if received_verify_token == VERIFY_TOKEN:
            return Response(body=challenge, status_code=200)
    
    # Process requests
    elif app.current_request.method == 'POST':

        payload = app.current_request.json_body
        message = payload['entry'][0]['messaging'][0]
        message_sender_id = message['sender']['id']
        message_text = message['message']['text']
        
        if message_text == 'Hello!':
            response = 'Hey from Messenger Bot!'
            bot.send_text_message(message_sender_id, response)

    return Response(body='success', status_code=200)
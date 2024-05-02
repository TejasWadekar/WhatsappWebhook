from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import requests

def sendWhatsAppMessage(phoneNumber, message):
    headers = {"Authorization": 'Bearer EAAFgGgvXsh4BO6tXRGyTAxduE7kf1182yBv4R7seNkhV6cWwn4Qpv6A5RIIqqiNhACNuQ5VfA5wekeqmcoeU2hpcWTh0HTuowWlBCr1qpxyAi8rpFKXFZBab3p7oc4co8Y0fZBqBq40Tpg2DdUkuBUCGY2NLzzZCDviZChNbgcZA5UlcnNlvaSTZBJGg9a9N6JP7W3Qh4Rb2gPjZCQe1SFCvmeGKd8ZD'}
    payload = {"messaging_product":"whatsapp",
               "recipient_type":"individual",
               "to":phoneNumber,
               "type": "text",
               "text": {"body":message}
               }
    response = requests.post('https://graph.facebook.com/v19.0/281227265076918/messages', headers=headers,json=payload)
    ans = response.json()
    return ans






@csrf_exempt #rather than using DRF we can use this
def whatsAppWebhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = 'e58b84b9-3017-4d13-be4e-04c05e50a353'
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            # return HttpResponse(challenge, status = 200)
            return HttpResponse(request.GET.get('hub.challenge'), status=200)
        else:
            return HttpResponse('error', status =403)
        
    #Used for receiving the message
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        phoneNumber = entry['changes'][0]["value"]['metadata']['display_phone_number']
                        phoneId = entry['changes'][0]["value"]['metadata']['phone_number_id']
                        profileName = entry['changes'][0]["value"]['contacts'][0]['profile']['name']
                        whatsAppId = entry['changes'][0]["value"]['contacts'][0]['wa_id']
                        formId = entry['changes'][0]["value"]['messages'][0]['form']
                        messageld = entry['changes'][0]["value"]['messages'][0]['id']
                        timestamp = entry['changes'][0]["value"]['messages'][0]['timestamp']
                        text = entry['changes'][0]["value"]['messages'][0]['text']['body']

                        phoneNumber = "+917058921518"
                        message = f'{text} was received'
                        sendWhatsAppMessage(phoneNumber, message)
                except:
                    pass

        return HttpResponse('success', status = 200)
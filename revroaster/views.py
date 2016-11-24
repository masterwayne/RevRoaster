from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
from .forms import URLForm
import sentiment_mod as s
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json, requests, random, re
from pprint import pprint
import urllib
import simplejson as json
from .models import SavedUrl

dict_url = []
def reviews(request):
	if request.method == 'POST':
		url = request.POST.get('url')
		send_url = urllib.quote_plus(url)
		ini='http://api.diffbot.com/v3/article?token=a4cf77eca239a985bc6c0e41b5fa0011&url='+send_url
		res=requests.get(ini)
		data = json.loads(res.text)
		size = len(data['objects'][0]['discussion']['posts'])
		positive = []
		negative = []
		final_score = 0;
		name = data['objects'][0]['title']
		print(send_url)
		#name="shvabdjskfmbjdsaklsfdbasnjfsnjdfkjaknsnvxxnjdfsnjdfnndfsfjbjnsdskmdkmfskmdgknfk"
		for i in range(0,size):
			review = {}
			sentiment_value, confidence = s.sentiment(data['objects'][0]['discussion']['posts'][i]['text'].encode('ascii','ignore'))
			check = data['objects'][0]['discussion']['posts'][i]['text'].encode('ascii','ignore')
			review.update({'review':data['objects'][0]['discussion']['posts'][i]['text'].encode('ascii','ignore'),'name':data['objects'][0]['discussion']['posts'][i]['author']})
			final_score = final_score + confidence
			flag = 0 ;
			bad_words = ["disappointment","disappoint","bad","worse","worst","not good","awfull","not happy","costly","poor","misleading","horrible","slow","now working","badly"]
			for word in bad_words:
				if word in check:
					flag=1
			if sentiment_value == "pos" and flag == 0:
				positive.append(review)
			else:	
				negative.append(review)
		rating = [2.8,3.2,3.5,3.7,3.8,4.2,4.4,4.6];
		pos_size = len(positive)
		neg_size = len(negative)
		final_score = rating[pos_size - neg_size]
		ini='http://api.diffbot.com/v3/product?token=a4cf77eca239a985bc6c0e41b5fa0011&url='+send_url	
		res = requests.get(ini)
		data = json.loads(res.text)
		image = data['objects'][0]['images'][0]['url']
		entry = SavedUrl(url=send_url,name=name,image=image)
		entry.positive = json.dumps(positive)
		entry.negative = json.dumps(negative)
		entry.save()
		jsonDec = json.decoder.JSONDecoder()
		all_entries = SavedUrl.objects.all()
		for entries in all_entries:
			if entries is not None:
				if entries.positive is not None:
					myPythonList = jsonDec.decode(entries.positive)
					for pos in myPythonList:
						print(pos['review'])
						print("                                                 ")
        return render(request, 'revroaster/searchpage2.html',{'url':url,'name':name,'positive':positive,'negative':negative,'score':final_score,'image':image})
def home(request):
    # if this is a POST request we need to process the form data
	return render(request, 'revroaster/searchpage.html')

class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '1234':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        message = incoming_message['entry'][0]['messaging'][0]
        if 'message' in message and message['message']['text'] is not None:
        	url = message['message']['text']
        	send_url = urllib.quote_plus(url)
        	flag = 0
        	print(send_url)
        	#user_details_url = "https://graph.facebook.com/v2.6/%s"%message['sender']['id']
        	#user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAFsq1Lzxt4BADZBrGfZBd9LyEeX7gtb2aiKFpOluZAaMsDN2FTSEflg5B1frlmBuZC8xR5BOnngekPynQ2ZBC9mF1qMYOJdc5IN0NWJsESqZAXZBGRrniSFEfc3x2gonc23K6ZA8lMldhhlMfLA7QxvGn5Jb7PRrrZC5ZB1I48pZBjsxuRlUTEA326'}
        	#user_details = requests.get(user_details_url, user_details_params).json()
        	print(user_details)
        	all_entries = SavedUrl.objects.all()

        	for entries in all_entries:
        		#post_facebook_message(message['sender']['id'], entries.url)
        		if entries.url == send_url:
        			flag=1
        			post_facebook_message(message['sender']['id'], entries.name)
        			post_facebook_image(message['sender']['id'], entries.image)
        			jsonDec = json.decoder.JSONDecoder()
        			myPythonList = jsonDec.decode(entries.positive)
        			psize = len(myPythonList)
        			for i in range(0,psize):
        				temp = myPythonList[i]['review'].encode('ascii','ignore')[0:200]
        				post_facebook_message(message['sender']['id'], temp)
        			
        			myPythonNegative = jsonDec.decode(entries.positive)
        			psize = len(myPythonNegative)
        			for i in range(0,psize):
        				temp = myPythonNegative[i]['review'].encode('ascii','ignore')[0:200]
        				post_facebook_message(message['sender']['id'], temp)
        			
        			break

        	if flag == 0:
        		ini='http://api.diffbot.com/v3/article?token=a4cf77eca239a985bc6c0e41b5fa0011&url='+send_url
        		res=requests.get(ini)
        		data = json.loads(res.text)
        		print(url)
        		post_facebook_message(message['sender']['id'], data['objects'][0]['title'])
        		i_url='http://api.diffbot.com/v3/product?token=a4cf77eca239a985bc6c0e41b5fa0011&url='+send_url	
        		ires = requests.get(i_url)
        		idata = json.loads(ires.text)
        		image = idata['objects'][0]['images'][0]['url']	
        		post_facebook_message(message['sender']['id'], pdata['objects'][0]['offerPrice'])
        		size = len(data['objects'][0]['discussion']['posts'])
        		post_facebook_image(message['sender']['id'],image)
        		for i in range(0,size):
        			temp = data['objects'][0]['discussion']['posts'][i]['text'].encode('ascii','ignore')
        			review = temp[0:200]
        			post_facebook_message(message['sender']['id'], review)
        	
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        #for entry in incoming_message['entry']:
            #for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
        #if 'message' in message:
                    # Print the message to the terminal
                    #url = message['message']['text']
                    #send_url = urllib.quote_plus(url)
                    #ini='http://api.diffbot.com/v3/article?token=a4cf77eca239a985bc6c0e41b5fa0011&url='+send_url
                    #res=requests.get(ini)
                    #data = json.loads(res.text)
                    #print(url)
                    #post_facebook_message(message['sender']['id'], data['objects'][0]['title'])
                    #size = len(data['objects'][0]['discussion']['posts'])
                    #for i in range(0,size):
                    	#temp = data['objects'][0]['discussion']['posts'][i]['text'].encode('ascii','ignore')
                    	#review = temp[0:200]
                    	#post_facebook_message(message['sender']['id'], review) 
        #post_facebook_message(message[0]['sender']['id'], "hello")    
        return HttpResponse()

def post_facebook_message(fbid, recevied_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAFsq1Lzxt4BADZBrGfZBd9LyEeX7gtb2aiKFpOluZAaMsDN2FTSEflg5B1frlmBuZC8xR5BOnngekPynQ2ZBC9mF1qMYOJdc5IN0NWJsESqZAXZBGRrniSFEfc3x2gonc23K6ZA8lMldhhlMfLA7QxvGn5Jb7PRrrZC5ZB1I48pZBjsxuRlUTEA326' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
def post_facebook_image(fbid, url):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAFsq1Lzxt4BADZBrGfZBd9LyEeX7gtb2aiKFpOluZAaMsDN2FTSEflg5B1frlmBuZC8xR5BOnngekPynQ2ZBC9mF1qMYOJdc5IN0NWJsESqZAXZBGRrniSFEfc3x2gonc23K6ZA8lMldhhlMfLA7QxvGn5Jb7PRrrZC5ZB1I48pZBjsxuRlUTEA326' 
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"image","payload":{"url":url}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	pprint(status.json())
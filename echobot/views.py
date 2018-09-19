from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from categories.exchange_rate import ExchangeRate
from config.config import LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt    
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                #sender = event.source.sender_id
                #print(line_bot_api.get_profile(sender))
                new_text = define_text(event.message.text)
                line_bot_api.reply_message(
                   event.reply_token,
                   TextSendMessage(text=new_text)
                )
        
        return HttpResponse()
        
    else:
        return HttpResponseBadRequest()

def define_text(text):
    re_text = text
    if text.startswith('$'):
        ex_r = ExchangeRate(text[1:].upper())
        re_text = ex_r.msg if ex_r.msg else '無法判斷'
        
    return re_text
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import web_page_summary_form, text_summary_form
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
import sys, os
from newspaper import Article
import nltk
nltk.download('punkt')
from .forms import ServicesForm, contactForm 



def About(request):
    context ={}
    template = 'services/about.html'
    return render(request, template, context)

def Contact(request):
    title = 'CONTACT US'
    form = contactForm(request.POST or None)
    confirm_message = " we are eager to hear from you! get in touch with the Admin directly through this form"	
    if form.is_valid():
        name = form.cleaned_data['name']   
        email = form.cleaned_data['email']      
        comment = form.cleaned_data['comment']
        subject = 'message from TalesArena Contact'
        message = '%s %s %s' %(comment, email, name)
        emailFrom = 'contact@talesarena.com'
        emailTo = ['mytalesrena@gmail.com']
        send_mail(subject, message, emailFrom, emailTo,  fail_silently = True),
        title = "THANKS"
        confirm_message = "For reaching out we will get back to you shortly"  
        form = None     
    context = {'form':form, 'title': title, 'confirm_message': confirm_message,}
    template = 'services/contact.html'
    return render(request, template, context)



def Services(request):
    title = 'SERVICE SUBSCRIPTION FORM'
    form = ServicesForm(request.POST or None)
    confirm_message = "Your Satisfaction is Our Inspiration"	
    if form.is_valid():
        name = form.cleaned_data['name'] 
        email = form.cleaned_data['email']  
        phone_number = form.cleaned_data['phone_number']      
        service = form.cleaned_data['service'] 
        description = form.cleaned_data['description']       
        subject = 'message from  TalesArena Services'
        message = '%s %s %s %s %s' %(service, description, email, name, phone_number)
        emailFrom = 'service@talesarena.com'
        emailTo = ['mytalesrena@gmail.com']
        send_mail(subject, message, emailFrom, emailTo,  fail_silently = True),
        title = "Thanks"
        confirm_message = "We Will Get Back To You Shortly!"   
        form = form.save     
        form = None
    context = {'form':form, 'title': title, 'confirm_message': confirm_message,}
    template = 'services/service.html'
    return render(request, template, context)





def Summary(request):
    text_kw = None 
    text_results = None
    keyWords = None
    results = None
    w_form = web_page_summary_form(request.POST or None)
    t_form = text_summary_form(request.POST or None)
    if w_form.is_valid():          
        url = w_form.cleaned_data['SUMMARIZE']
        LANGUAGE = w_form.cleaned_data['LANGUAGE']
        SENTENCES_COUNT = w_form.cleaned_data['SENTENCES_COUNT'] 
        try:            
            article = Article(url)                        
            article.download()
            article.parse() 
            article.nlp()
            keyWords = article.keywords
             
            parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))       
            stemmer = Stemmer(LANGUAGE)
            summarizer = Summarizer(stemmer)
            summarizer.stop_words = get_stop_words(LANGUAGE)       
            results = summarizer(parser.document, SENTENCES_COUNT)
        except:                   
            keyWords = 'Invalid Entry'
            results = '-'   
            pass
              

    if t_form.is_valid():
        Text_field = t_form.cleaned_data['Text_field']
        Lang = t_form.cleaned_data['Lang']
        s_counts =  t_form.cleaned_data['s_counts'] 

        try:
            with open('textfile.txt', 'w', encoding="utf-8") as f:
                f.write(Text_field)
            text_parser = PlaintextParser.from_file('textfile.txt', Tokenizer(Lang))
            text_stemmer = Stemmer(Lang)
            text_summarizer = Summarizer(text_stemmer)
            text_summarizer.stop_words = get_stop_words(Lang)
            text_results = text_summarizer(text_parser.document, s_counts) 
               
        except:
            text_kw = None 
            text_results = ["'_'"]

        
    context = {
            't_form':t_form,
            'w_form':w_form,
            'keywords':keyWords,
            'results':results,
            'text_kw': text_kw,
            'text_results': text_results          
           }
    template = 'services/summarizer.html'
    return render(request, template, context)
    
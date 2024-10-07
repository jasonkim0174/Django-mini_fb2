## quotes/views.py
## description: write view functions to handle URL requests fro the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time

QUOTES = [
    "I think, team first. It allows me to succeed, it allows my team to succeed.",
    "You can't be afraid to fail. It's the only way you succeed—you're not gonna succeed all the time, and I know that.",
    "I like criticism. It makes you strong.",
    "I'm going to use all my tools, my God-given ability, and make the best life I can with it.",
    "In Northeast Ohio, nothing is given. Everything is earned. You work for what you have."
    "I always say, decisions I make, I live with them. There's always ways you can correct them or ways you can do them better. At the end of the day, I live with them.",
    "I treat my first like my last, and my last like my first.",
    "It's our ball aint it.",
    "Can't believe this is my life",
    "I don't know how tall I am or how much I weigh. Because I don't want anybody to know my identity. I'm like a superhero. Call me Basketball Man."
]

IMAGES = [
    "https://m.media-amazon.com/images/I/81MoV7qLkrL.jpg",
    "https://cdn.vox-cdn.com/thumbor/PHCxvBW5jEN_-r7EuyG7am-ZuNw=/0x40:960x680/1820x1213/filters:focal(0x40:960x680):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/10416343/lebronnn.0.jpg",
    "https://deadline.com/wp-content/uploads/2022/08/Lebron-James.jpg",
    "https://www.stack.com/wp-content/uploads/2016/11/12031516/17n8tlutsv1gpjpg.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQh_v59lE2-Kiwvr9B8rUOqyu2ojdLGRJMWlA&s",
    "https://ih1.redbubble.net/image.5498349439.8099/raf,360x360,075,t,fafafa:ca443f4786.jpg"
]


# Create your views here.
# def main(request):
#     '''Handle the main URL for the quotes app'''

#     response_text = '''
#     '''

#     HttpResponse(response_text)

def quote(request):
    '''
    Function to handle the URL request for /quote (main page).
    Delegate rendering to the template hw/quote.html.
    '''
    # Render the response
    template_name = 'quotes/quote.html'

    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)

    context = {
        'current_time' : time.ctime(),
        'quote': quote,
        'image': image
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    '''
    Function to handle the URL request for /show_all (main page).
    Delegate rendering to the template hw/show_all.html.
    '''
    # Render the response
    template_name = 'quotes/show_all.html'

    context = {
        "current_time" : time.ctime(),
        'quotes': QUOTES,
        'images': IMAGES
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /about (main page).
    Delegate rendering to the template hw/about.html.
    '''
    # Render the response
    template_name = 'quotes/about.html'

    context = {
        "current_time" : time.ctime()
    }

    # Delegate rendering work to the template
    return render(request, template_name, context)
import random
import time
from django.shortcuts import render
from datetime import timedelta
from django.utils.timezone import now

# View for the main page
def main(request):
    context = {
        'restaurant_name': 'Booming Brunch',
        'location': '10 Buick Street, Boston, MA',
        'hours': [
            ('Monday-Saturday', '9 AM - 9 PM'),
        ],
        'photos': ['brunch.jpg'],  
        "current_time" : time.ctime(),
    }
    return render(request, 'restaurant/main.html', context)

# View for the order page
def order(request):
    # List of daily specials
    specials = ['French Toast of the Day', 'Pancake of the Day', 'Waffle of the Day', 'Burger Combo']
    daily_special = random.choice(specials)

    context = {
        'menu_items': [
            {'name': 'French Toast', 'price': 8, 'options': ['Extra Toast', 'Strawberries', 'Fruit Combo']},
            {'name': 'Pancakes', 'price': 6, 'options': ['Whipped Cream', 'Bacon']},
            {'name': 'Waffles', 'price': 7, 'options': ['Blueberries', 'Banana foster', 'Fried Chicken']},
            {'name': 'Daily Special', 'price': 12, 'special': daily_special}
        ],
         "current_time" : time.ctime(),
    }
    return render(request, 'restaurant/order.html', context)

# View for the confirmation page
def confirmation(request):
    if request.method == 'POST':
        items_ordered = request.POST.getlist('menu_items')
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')

        # Calculate total price
        prices = {
            'French Toast': 8,
            'Pancakes': 6,
            'Waffles': 7,
            'Daily Special': 12,
        }
        total_price = sum([prices[item] for item in items_ordered])

        # Determine order ready time
        ready_time_minutes = random.randint(30, 60)
        ready_time = now() + timedelta(minutes=ready_time_minutes)

        context = {
            'items_ordered': items_ordered,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%I:%M %p'),
             "current_time" : time.ctime(),
        }
        return render(request, 'restaurant/confirmation.html', context)

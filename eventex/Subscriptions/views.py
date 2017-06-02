from django.shortcuts import render
from eventex.Subscriptions.forms import SubscriptionForm


def subscribe(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'Subscriptions/subscription_form.html', context)

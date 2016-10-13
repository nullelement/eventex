from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    _send_mail('Confirmação de inscrição',
               settings.DEFAULT_FROM_EMAIL,
               subscription.email,
               'subscriptions/subscription_email.txt',
               {'subscription': subscription})

    #masked_id = int(subscription.pk) ^ 0xABCDEFAB
    masked_id = int(subscription.pk) # Desabilitar a ofuscagem de ID. Está me atrapalhando seguir o curso.

    return HttpResponseRedirect('/inscricao/{}/'.format(masked_id))


def new(request):
    return render(request, 'subscriptions/subscription_form.html',
                  {'form': SubscriptionForm()})

def detail(request, pk):
    unmasked_id = int(pk) ^ 0xABCDEFAB
    unmasked_id = int(pk) # Desabilitar a afosucagem de ID. Está me atrapalhando seguir o curso.

    try:
        subscription = Subscription.objects.get(pk=unmasked_id)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html', {'subscription':subscription})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])

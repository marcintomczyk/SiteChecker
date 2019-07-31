import asyncio
from threading import Thread

import aiohttp
from aiohttp import ClientConnectionError
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render
from django.utils import timezone

from site_checker.models import Site


def index(request):
    return render(request, 'site_checker/checker.html', {})


def start_loop(loop, original_site_address):
    asyncio.set_event_loop(loop)
    site_response = loop.run_until_complete(check_site_status(original_site_address))
    create_site_details(original_site_address, site_response)


async def check_site_status(url):
    # TODO: introduce logging
    # BUT it requires having correct settings in the main project
    # so without configuring it log.debug's statements would be not visible
    # this is why for now I am using print for 'marking' starting
    #print('Starting {}'.format(url))
    connector = aiohttp.TCPConnector(verify_ssl=False)
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            return await session.head(url, allow_redirects=True)
    # TODO: we could also catch another exceptions such as HTTPError, Timeouts, TooManyRedirects
    # TODO: Maybe use RequestException ?
    except ClientConnectionError as cce:
        return cce


def create_site_details(original_site_address, response):
    if hasattr(response, 'status') and hasattr(response, 'url'):
        site = Site.objects.create(original_address=original_site_address,
                                   final_address=response.url,
                                   status_code=response.status,
                                   check_date=timezone.now())
    # means we got an exception as a response
    else:
        site = Site.objects.create(original_address=original_site_address,
                                   status_code=0,
                                   check_date=timezone.now(),
                                   error_message=response)
    return site


def check(request):
    site_address = request.POST['site_address']
    try:
        validate = URLValidator()
        validate(site_address)
    except ValidationError:
        return render(request, 'site_checker/checker.html', {
            'message': 'Invalid url',
        })

    loop = asyncio.new_event_loop()
    # I don't want to block the current django thread (the main thread)
    # instead I would like to 'sent' something to be done regardless of the current thread
    # so the page is more responsive etc.
    # it can be done also in other ways ie: with Celery, Django Channels
    # but as I didn't know async/await I just wanted to dive a bit into it
    # and see how it behaves with Django (which is synchronous by nature)
    t = Thread(target=start_loop, args=(loop, site_address))
    t.start()

    return render(request, 'site_checker/checker.html', {
        'message': "The request was sent for execution",
        'time_of_the_message': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    })

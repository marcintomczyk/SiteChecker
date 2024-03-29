
import asyncio
from datetime import datetime
from threading import Thread

import aiohttp
import json
from aiohttp import ClientConnectionError
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from site_checker.models import Site

SITE_CHECKER_MAIN_URL = 'site_checker/checker.html'
SITE_CHECKER_CHANNEL_MAIN_ROOM = 'ws://localhost:8000/ws/checker_channel/main_room/'



# yes, I know I could use Class-based views :) but haven't used them intentionally
def index(request):
    return render(request, SITE_CHECKER_MAIN_URL, {})


def start_loop(loop, original_site_address):
    asyncio.set_event_loop(loop)
    site_response = loop.run_until_complete(check_site_status(original_site_address))

    #TODO: introduce chaining
    loop.run_until_complete(send_ws_message(prepare_message(original_site_address, "checking finished, status: "
                                                            + str(site_response.status))))

    create_site_details(original_site_address, site_response)


async def check_site_status(url):

    await send_ws_message(prepare_message(url, "preparing for checking site"))

    # TODO: introduce logging
    # BUT it requires having correct settings in the main project
    # so without configuring it log.debug's statements would be not visible
    # this is why for now I am using print for 'marking' starting
    #print('Starting {}'.format(url))

    # TODO: give the ability to configure turning on/off ssl verification
    # in real projects this setting could be set up on 'url' level (some kind of configuration)
    # or we could check if the domains are similar ie: in case of facebook it is not a problem
    # when we got certificate from facebook.com where expecting facebook.pl
    # other sites might be more problematic and unsafe however fetching only via head is much safer
    # than via get (but of course the text we get is not dangerous itself. The problem lies
    # in where and how this text would be used)
    connector = aiohttp.TCPConnector(verify_ssl=False)
    try:
        await send_ws_message(prepare_message(url, "checking site started"))

        async with aiohttp.ClientSession(connector=connector) as session:
            return await session.head(url, allow_redirects=True)
    # TODO: we could also catch another exceptions such as HTTPError, Timeouts, TooManyRedirects
    # TODO: Maybe use RequestException ?
    except ClientConnectionError as cce:
        return cce


async def send_ws_message(message):
    async with aiohttp.ClientSession() as ws_session:
        async with ws_session.ws_connect(SITE_CHECKER_CHANNEL_MAIN_ROOM) as ws:
            await ws.send_str(message)
            ws.close()
        await ws_session.close()


def create_site_details(original_site_address, response):
    if hasattr(response, 'status') and hasattr(response, 'url'):
        site = Site.objects.create(original_address=original_site_address,
                                   final_address=response.url,
                                   status_code=response.status,
                                   check_date=datetime.timestamp(datetime.now()))
    # means we got an exception as a response
    else:
        site = Site.objects.create(original_address=original_site_address,
                                   status_code=0,
                                   error_message=response,
                                   check_date=datetime.timestamp(datetime.now()))
    return site


def check(request):

    if request.method != 'POST':
        return render(request, SITE_CHECKER_MAIN_URL, {
            'message': 'This kind of request ie: {} currently not supported'.format(request.method),
        })

    site_address = request.POST['site_address']
    try:
        validate = URLValidator()
        validate(site_address)
    except ValidationError:
        return render(request, SITE_CHECKER_MAIN_URL, {
            'message': 'Invalid url',
        })

    loop = asyncio.new_event_loop()
    # I don't want to block the current django thread (the main thread)
    # instead I would like to 'sent' something to be done regardless of the current thread
    # so the page is more responsive etc.
    # it can be done also in other ways ie: with Celery, Django Channels
    # but as I didn't know async/await I just wanted to dive a bit into it
    # and see how it behaves with Django (which is synchronous by nature)

    # NOTE !!!!!!!
    # in a real app I would go rather in a bit different solution but it wouldn't be a simple app then:
    # clicking a button on the form would create a new site in db with initial data only (ie: in simplest form only url)
    # I would use another component of the system ie: could be celery for example
    # or even a background process running constantly and fetching new site entries in db
    # having the site entry the process would make the real check, saving the result in the db (record's update)
    # this way we could separate django view and check process so we could also eliminate
    # things like creating a separate thread here
    # BUT as I wrote a bit above I just wanted to do/learn something else/new
    # ie: how Django cooperates with async/await (further extensions could be Django channels)
    t = Thread(target=start_loop, args=(loop, site_address))
    t.start()

    #return render(request, 'site_checker/checker.html', {
    #    'message': "The request was sent for execution",
    #    'time_of_the_message': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    #})

    return HttpResponse(json.dumps({
        'message': "The request was sent for execution",
        'time_of_the_message': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    }))


def prepare_message(url, message):
    request_data = {'url': str(url),
                    'message': message,
                    'timestamp': str(timezone.now())
                    }
    return json.dumps(request_data)

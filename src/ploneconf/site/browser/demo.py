from Products.Five import BrowserView
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

import json
import logging
import requests

logger = logging.getLogger(__name__)


class DemoContent(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        self.create_talks(portal)
        return self.request.response.redirect(portal.absolute_url())

    def create_talks(self, container, amount=5):
        """Create some talks"""

        alsoProvides(self.request, IDisableCSRFProtection)
        plone_view = api.content.get_view('plone', self.context, self.request)
        jokes = self.random_jokes(amount)
        for data in jokes:
            joke = data['joke']
            talk = api.content.create(
                container=container,
                type='talk',
                title=plone_view.cropText(joke, length=20),
                description=joke,
                type_of_talk='Talk',
            )
            api.content.transition(talk, to_state='published')
            logger.info(f'Created talk {talk.absolute_url()}')
        api.portal.show_message(f'Created {amount} talks!', self.request)

    def random_jokes(self, amount):
        jokes = requests.get(f'http://api.icndb.com/jokes/random/{amount}')
        return json.loads(jokes.text)['value']

# encoding=utf-8
from plone import api
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import Interface
from zope.interface import provider

class IVotableLayer(Interface):
    """Marker interface for the Browserlayer of this addon
    """

# IVotable is the marker interface for contenttypes who support this behavior
class IVotable(Interface):
    pass

# This is the behavior interface.
# When doing IVoting(object), you receive an adapter
@provider(IFormFieldProvider)
class IVoting(model.Schema):
    if not api.env.debug_mode():
        directives.omitted("votes")
        directives.omitted("voted")

    fieldset(
        'debug',
        label=u'debug',
        fields=('votes', 'voted'),
    )

    votes = schema.Dict(title=u"Vote info",
                        key_type=schema.TextLine(title=u"Voted number"),
                        value_type=schema.Int(title=u"Voted so often"),
                        required=False,
                        default={},
                        missing_value={},
                        )
    voted = schema.List(title=u"Vote hashes",
                        value_type=schema.TextLine(),
                        required=False,
                        default=[],
                        missing_value=[],
                    )

    def vote(request):
        """
        Store the vote information, store the request hash to ensure
        that the user does not vote twice
        """

    def average_vote():
        """
        Return the average voting for an item
        """

    def has_votes():
        """
        Return whether anybody ever voted for this item
        """

    def already_voted(request):
        """
        Return the information wether a person already voted.
        This is not very high level and can be tricked out easily
        """

    def clear():
        """
        Clear the votes. Should only be called by admins
        """

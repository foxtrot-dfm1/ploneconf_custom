from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


LevelVocabulary = SimpleVocabulary(
    [SimpleTerm(value='platinum', title='Platinum Sponsor'),
     SimpleTerm(value='gold', title='Gold Sponsor'),
     SimpleTerm(value='silver', title='Silver Sponsor'),
     SimpleTerm(value='bronze', title='Bronze Sponsor')]
    )


class ISponsor(model.Schema):
    """Dexterity Schema for Sponsors
    """

    directives.widget(level=RadioFieldWidget)
    level = schema.Choice(
        title='Sponsoring Level',
        vocabulary=LevelVocabulary,
        required=True
    )

    text = RichText(
        title='Text',
        required=False
    )

    url = schema.URI(
        title='Link',
        required=False
    )

    fieldset('Images', fields=['logo', 'advertisement'])
    logo = namedfile.NamedBlobImage(
        title='Logo',
        required=False,
    )

    advertisement = namedfile.NamedBlobImage(
        title='Advertisement (Gold-sponsors and above)',
        required=False,
    )

    directives.read_permission(notes='cmf.ManagePortal')
    directives.write_permission(notes='cmf.ManagePortal')
    notes = RichText(
        title='Secret Notes (only for site-admins)',
        required=False
    )

@implementer(ISponsor)
class Sponsor(Container):
    """Sponsor instance class"""
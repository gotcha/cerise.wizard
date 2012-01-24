from zope.interface import Interface

from zope import schema

from cerise.wizard.utils import CeriseMessageFactory as _


class IFirst(Interface):

    first = schema.TextLine(
        title=_(u'First'),
        description=_(u'First field described'),
        required=False,
        missing_value=u'',
        )


class ISecond(Interface):

    second = schema.Bool(
        title=_(u'Second'),
        required=False,
        )


class IChoice(Interface):

    choice = schema.Choice(
        title=_(u'Choice'),
        values=(u'first', u'second'),
        default=u'first'
        )

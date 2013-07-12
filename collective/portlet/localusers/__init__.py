from zope.i18nmessageid import MessageFactory
LocalUsersMessageFactory = MessageFactory('collective.portlet.localusers')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

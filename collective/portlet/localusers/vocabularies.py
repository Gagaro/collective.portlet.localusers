from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from collective.portlet.localusers import LocalUsersMessageFactory as _


roles = SimpleVocabulary([
    SimpleTerm(u'Role 1', _(u"Role 1")),
    SimpleTerm(u'Role 2', _(u"Role 2")),
    SimpleTerm(u'Role 3', _(u"Role 3")),
])

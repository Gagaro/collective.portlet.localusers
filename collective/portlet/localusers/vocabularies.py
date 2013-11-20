from plone.i18n.normalizer.base import baseNormalize
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from collective.portlet.localusers import LocalUsersMessageFactory as _


def localRoles(context):
    roles = [
        SimpleTerm(
            baseNormalize(role),
            baseNormalize(role),
            _(role),
            ) for role in sorted(context.valid_roles())
        ]
    return SimpleVocabulary(roles)

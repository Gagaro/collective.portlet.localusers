from zope import interface
from zope import schema
from z3c.form.browser.select import SelectFieldWidget

from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.localusers import LocalUsersMessageFactory as _


class ILocalUsers(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(
        title=_(u"Header"),
        required=False,
    )

    directives.widget('roles', SelectFieldWidget, multiple='multiple')
    roles = schema.List(
        title=_("Roles"),
        description=_("The users with these roles will be shown.\
        If none are selected, it will show users from all roles."),
        required=False,
        value_type=schema.Choice(
            vocabulary='collective.portlet.localusers.vocabularies.localroles'
        ),
    )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    interface.implements(ILocalUsers)

    header = _(u'Local Users')

    roles = []

    def __init__(self, header=None, roles=[]):
        self.header = header
        self.roles = roles

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header or _(u"Local Users")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('localusers.pt')

    def getUsersName(self):
        valid_roles = self.context.valid_roles()
        users = []
        for role in valid_roles:
            if not self.data.roles or role in self.data.roles:
                users += self.context.users_with_local_role(role)
        return sorted(set(users))

    def getUsers(self):
        users_name = self.getUsersName()
        mtool = getToolByName(self.context, 'portal_membership')
        users = []
        for user in users_name:
            member = mtool.getMemberById(user)
            if member is not None:
                users.append(member)
        return users


class AddForm(AutoExtensibleForm, z3cformhelper.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    schema = ILocalUsers
    enableCSRFProtection = True

    def create(self, data):
        return Assignment(**data)


class EditForm(AutoExtensibleForm, z3cformhelper.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    schema = ILocalUsers
    enableCSRFProtection = True

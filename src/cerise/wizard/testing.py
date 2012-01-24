from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CeriseWizard(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import cerise.wizard
        xmlconfig.file('configure.zcml',
                       cerise.wizard,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cerise.wizard:default')

CERISE_WIZARD_FIXTURE = CeriseWizard()
CERISE_WIZARD_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(CERISE_WIZARD_FIXTURE, ),
                       name="CeriseWizard:Integration")
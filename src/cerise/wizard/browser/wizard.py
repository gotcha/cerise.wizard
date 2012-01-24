from z3c.form import field

from collective.z3cform.wizard import wizard

from cerise.wizard.utils import CeriseMessageFactory as _
from cerise.wizard.interfaces import IFirst
from cerise.wizard.interfaces import ISecond
from cerise.wizard.interfaces import IChoice

from zope.component import queryUtility

from plone.registry.interfaces import IRegistry

from plone.z3cform import layout


class FirstStep(wizard.Step):
    prefix = 'first'
    label = _(u'First')
    fields = field.Fields(IFirst)

    def load(self, context):
        data = self.getContent()
        registry = queryUtility(IRegistry)
        first = registry.forInterface(IFirst)
        value = first.first
        data.setdefault('first', value)


class SecondStep(wizard.Step):
    prefix = 'second'
    label = _(u'Second')
    fields = field.Fields(ISecond)

    def load(self, context):
        data = self.getContent()
        registry = queryUtility(IRegistry)
        second = registry.forInterface(ISecond)
        data.setdefault('second', second.second)


class ChoiceStep(wizard.Step):
    prefix = 'choice'
    label = _(u'Choice')
    fields = field.Fields(IChoice)


class SecondChoiceStep(wizard.Step):
    prefix = 'second_choice'
    label = _(u'Second Choice')
    fields = field.Fields(IChoice)


class Wizard(wizard.Wizard):
    label = _(u'Cerise Wizard')

    @property
    def steps(self):
        if self.choice == u'second':
            if not self.second_choice:
                return [ChoiceStep, SecondChoiceStep, FirstStep]
            elif self.second_choice == u'second':
                return [ChoiceStep, SecondChoiceStep, SecondStep]
            else:
                return [ChoiceStep, SecondChoiceStep, FirstStep]
        else:
            return [ChoiceStep, FirstStep]

    def showFinish(self):
        return (self.choice == u'first' or self.second_choice) and self.allStepsFinished

    @property
    def choice(self):
        choice_data = self.session.get('choice', {})
        choice = choice_data.get('choice', None)
        if 'choice.widgets.choice' in self.request.form:
            choice = unicode(self.request.form['choice.widgets.choice'][0])
        return choice

    @property
    def second_choice(self):
        choice_data = self.session.get('second_choice', {})
        choice = choice_data.get('choice', None)
        if 'second_choice.widgets.choice' in self.request.form:
            choice = unicode(self.request.form['second_choice.widgets.choice'][0])
        return choice

    def finish(self):
        registry = queryUtility(IRegistry)
        data = self.session
        if self.choice == u'first':
            first = registry.forInterface(IFirst)
            first.first = data[FirstStep.prefix]['first']
        elif self.choice == u'second':
            second = registry.forInterface(ISecond)
            second.second = data['second']['second']
        next_url = self.context.absolute_url() + '/portal_registry'
        self.request.RESPONSE.redirect(next_url)

WizardView = layout.wrap_form(Wizard)

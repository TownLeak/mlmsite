from django import forms
from mlmsite.controller import Controller
from mlmsite.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class IsPaymentIncluded(forms.Form):
    ok = forms.BooleanField(initial=True)


class GraphEval_SponsorSelectionForm(forms.Form):
    sponsor = UserModelChoiceField(queryset=User.objects.filter(isActive=True))

    def save(self):
        Controller().createNewUser(self.cleaned_data['sponsor'])


class GraphEval_UserSelectionForm(forms.Form):
    user = UserModelChoiceField(queryset=User.objects.filter(isActive=True))

    def save(self):
        Controller().setActualUser(self.cleaned_data['user'])

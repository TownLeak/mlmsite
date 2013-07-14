from django import forms
from controller import Controller
from models import User


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class GraphEval_SponsorSelectionForm(forms.Form):
    sponsor = UserModelChoiceField(queryset=User.objects.filter(isActive=True))

    def save(self):
        Controller().createNewUser(self.cleaned_data['sponsor'])


class GraphEval_UserSelectionForm(forms.Form):
    user = UserModelChoiceField(queryset=User.objects.filter(isActive=True))

    def save(self):
        Controller().setActualUser(self.cleaned_data['user'])

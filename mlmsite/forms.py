from django import forms
from controller import Controller
from models import User


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class GraphEval_SponsorSelectionForm(forms.Form):
    user = UserModelChoiceField(queryset=Controller.user_type.objects.filter(isActive=True))

    def save(self):
        c = Controller()
        user = User.CreateNewUser(sponsor=self.cleaned_data['user'])
        c.createNewBinaryPosition(user)


class GraphEval_UserSelectionForm(forms.Form):
    user = UserModelChoiceField(queryset=Controller.user_type.objects.filter(isActive=True))

    def save(self):
        c = Controller()
        c.setActualUser(self.cleaned_data['user'])

from django import forms
from controller import Controller


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class GraphEval_SponsorSelectionForm(forms.Form):
    user = UserModelChoiceField(queryset=Controller.user_type.objects.filter(isActive=True))

    def save(self):
        c = Controller()
        user = c.createNewUser(sponsor=self.cleaned_data['user'])
        c.createNewPosition(user)


class GraphEval_UserSelectionForm(forms.Form):
    user = UserModelChoiceField(queryset=Controller.user_type.objects.filter(isActive=True))

    def save(self):
        c = Controller()
        c.setActualUser(self.cleaned_data['user'])

from django import forms


class UserUpdateForm(forms.Form):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'pattern': '[A-Za-z ]+',
        'title': 'Only characters are allowed',
        'placeholder': 'Your first name',
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'pattern': '[A-Za-z ]+',
        'title': 'Only characters are allowed',
        'placeholder': 'Your last name',
    }), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'example@example.com'
    }), required=False)

    def __init__(self, user, data=None):
        super().__init__(data=data)
        self.initial['first_name'] = user.first_name
        self.initial['last_name'] = user.last_name
        self.initial['email'] = user.email

    def clean_email(self):
        return ''

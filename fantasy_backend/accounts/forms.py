
from ..contests.models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileRegistrationForm(UserCreationForm):
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('unspecified', 'Unspecified')],
        widget=forms.RadioSelect
    )
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)))
    country = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                gender=self.cleaned_data['gender'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                country=self.cleaned_data['country'],
                mobile=self.cleaned_data['mobile']
            )
        return user

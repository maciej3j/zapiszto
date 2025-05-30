from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import OrganizerRequest

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adres e-mail")
    request_organizer = forms.BooleanField(
        required=False,
        label="Chcę zostać organizatorem"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "request_organizer")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            student_group, _ = Group.objects.get_or_create(name="student")
            user.groups.add(student_group)
            if self.cleaned_data.get("request_organizer"):
                OrganizerRequest.objects.create(user=user)
        return user
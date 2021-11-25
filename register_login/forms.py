from django import forms
from online_forum.models import Author


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("full_name", "bio", "profile_pic")
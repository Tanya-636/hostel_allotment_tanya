from django import forms

class StudentSignupForm(forms.Form):
    registration_id = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    category = forms.ChoiceField(
        choices=[
            ("GENERAL", "General"),
            ("OBC", "OBC"),
            ("SC", "SC"),
            ("ST", "ST"),
            ("VJNT", "VJNT"),
        ]
    )
    cet_percentile = forms.DecimalField(
        max_digits=5, decimal_places=2
    )  # Allows for max 100.00
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class StudentLoginForm(forms.Form):
    registration_id = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)


class FacultyLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

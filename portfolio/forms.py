from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Your name",
            "class": "w-full px-4 py-3 border border-slate-300 dark:border-white/10 rounded-lg bg-transparent"
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "placeholder": "Your email (optional)",
            "class": "w-full px-4 py-3 border border-slate-300 dark:border-white/10 rounded-lg bg-transparent"
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Your message",
            "rows": 5,
            "class": "w-full px-4 py-3 border border-slate-300 dark:border-white/10 rounded-lg bg-transparent"
        })
    )

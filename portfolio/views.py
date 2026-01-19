from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse

from .models import Project, Skill, Profile
from .forms import ContactForm


def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    featured_projects = Project.objects.filter(is_featured=True)
    projects = Project.objects.filter(is_featured=False)

    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            reply_to = [email] if email else []

            email_message = EmailMessage(
                subject=f"New Portfolio Message from {name}",
                body=f"""
Sender Name: {name}
Sender Email: {email if email else 'Not provided'}

Message:
{message}
                """,
                from_email=settings.EMAIL_HOST_USER,
                to=["nishan.official22@gmail.com"],
                reply_to=reply_to,
            )
            email_message.send()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Message sent successfully!'})

    return render(request, "index.html", {
        "profile": profile,
        "skills": skills,
        "featured_projects": featured_projects,
        "projects": projects,
        "form": form,
    })

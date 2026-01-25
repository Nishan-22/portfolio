from django.shortcuts import render, redirect  # 1. Added redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse

from .models import Project, Skill, Profile, Certificate
from .forms import ContactForm

# ======================================================
# SHARED EMAIL LOGIC
# ======================================================
def send_contact_email(form):
    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]
    reply_to = [email] if email else []

    EmailMessage(
        subject=f"New Portfolio Message from {name}",
        body=f"Sender Name: {name}\nSender Email: {email or 'Not provided'}\n\nMessage:\n{message}",
        from_email=settings.EMAIL_HOST_USER,
        to=["nishan.official22@gmail.com"],
        reply_to=reply_to,
    ).send()

# ======================================================
# VIEWS
# ======================================================
def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    featured_projects = Project.objects.filter(is_featured=True)
    projects = Project.objects.filter(is_featured=False)
    certificates = Certificate.objects.all()
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_contact_email(form)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('home') # 2. Clear resubmission popup
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False}, status=500)

    return render(request, "index.html", {
        "profile": profile, "skills": skills, "featured_projects": featured_projects,
        "projects": projects, "certificates": certificates, "form": form,
    })

def terminal_view(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    certificates = Certificate.objects.all()
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_contact_email(form) # 3. Actually send the email
                return redirect('terminal') # 4. Clear resubmission popup
            except Exception as e:
                print(f"Error: {e}")

    return render(request, "terminal.html", {
        "profile": profile, "skills": skills, "projects": projects,
        "certificates": certificates, "form": form,
    })

# blockchain view remains the same...

def blockchain(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()

    return render(request, "blockchain.html", {
        "profile": profile,
        "skills": skills,
        "projects": projects,
    })
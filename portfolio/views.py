from django.shortcuts import render, redirect  # 1. Added redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse

from .models import Project, Skill, Profile, Certificate, BlogPost
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
    # All non-blockchain projects on home; featured first, then newest
    projects = Project.objects.filter(is_blockchain=False).order_by(
        "-is_featured", "-created_at"
    )
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
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "certificates": certificates,
        "form": form,
    })

def contact(request):
    profile = Profile.objects.first()
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_contact_email(form)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('contact')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False}, status=500)

    return render(request, "contact.html", {
        "profile": profile, "form": form,
    })

def terminal_view(request):
    # Only show blockchain projects in terminal view
    projects = Project.objects.filter(is_blockchain=True).order_by("-created_at")
    # Published posts only (toggle "Is published" in admin, or set when saving)
    blog_posts = BlogPost.objects.filter(is_published=True).order_by(
        "-published_at", "-created_at"
    )[:6]

    return render(request, "terminal.html", {
        "projects": projects, "blog_posts": blog_posts,
    })
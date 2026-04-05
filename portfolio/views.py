import logging

from django.shortcuts import render, redirect  # 1. Added redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)

from .models import Project, Skill, Profile, Certificate, BlogPost
from .forms import ContactForm


def _contact_inbox():
    return getattr(settings, "CONTACT_INBOX", "nishan.official22@gmail.com")


def _is_contact_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


# ======================================================
# SHARED EMAIL LOGIC
# ======================================================
def send_contact_email(form):
    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]
    reply_to = [email] if email else []

    if settings.EMAIL_BACKEND.endswith("smtp.EmailBackend"):
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise RuntimeError("SMTP is not configured (set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD).")
        from_email = settings.EMAIL_HOST_USER
    else:
        # Resend, console, etc.
        from_email = settings.DEFAULT_FROM_EMAIL

    EmailMessage(
        subject=f"New Portfolio Message from {name}",
        body=f"Sender Name: {name}\nSender Email: {email or 'Not provided'}\n\nMessage:\n{message}",
        from_email=from_email,
        to=[_contact_inbox()],
        reply_to=reply_to,
    ).send()


def _contact_post_response(request, form, redirect_name="contact"):
    """Return redirect, JsonResponse, or None (caller re-renders with current form)."""
    is_ajax = _is_contact_ajax(request)
    if not form.is_valid():
        if is_ajax:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return None

    try:
        send_contact_email(form)
    except Exception:
        logger.exception("Contact form: failed to send email")
        if is_ajax:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Could not send your message. Please try again later or email directly.",
                },
                status=500,
            )
        messages.error(
            request,
            "Could not send your message. Please try again or email directly.",
        )
        return None

    if is_ajax:
        return JsonResponse({"success": True})
    messages.success(request, "Your message was sent successfully.")
    return redirect(redirect_name)

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
        resp = _contact_post_response(request, form, redirect_name="home")
        if resp is not None:
            return resp

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
        resp = _contact_post_response(request, form)
        if resp is not None:
            return resp

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
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import AdminMailForm

# Create your views here.

def admin_mailer(request):
    recipients = []
    if request.method == 'POST':
        form = AdminMailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']

            for usr in User.objects.all():
                recipients.append(usr.email)
            send_mail(subject, message, sender, recipients)
        messages.success(request, "Mail successully sent to all users.")
        return redirect('/admin/auth/user')
    else:
        form = AdminMailForm()

    return render(request, 'admin/mail_page.html', {'form': form})
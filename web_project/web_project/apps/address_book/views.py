# addressbook/views.py

from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm
from django.shortcuts import render
from .models import Contact


def view_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'address_book/contact_detail.html', {'contact': contact})


def index_address_book(request):
    contacts = Contact.objects.all()
    return render(request, 'address_book/all_contacts.html', {'contacts': contacts})


def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_address_book')
    else:
        form = ContactForm()
    return render(request, 'address_book/contact_form.html', {'form': form})


def update_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('index_address_book')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'address_book/contact_form.html', {'form': form})


def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('index_address_book')
    return render(request, 'address_book/contact_confirm_delete.html', {'contact': contact})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import ContactForm
from index.models import Contact
from datetime import timedelta, datetime, date
from django.db.models import Q

@login_required
def index_address_book(request):
    query = request.GET.get('q', '').strip()
    if query:
        if ' ' in query:
            first_name, last_name = query.split(' ', 1)
            contacts = Contact.objects.filter(
                Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name),
                user=request.user
            ).order_by('id')
        else:
            contacts = Contact.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query),
                user=request.user
            ).order_by('id')
    else:
        contacts = Contact.objects.filter(user=request.user).order_by('id')
    
    paginator = Paginator(contacts, 10)  # количество контактов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    index = page_obj.number - 1  # индекс текущей страницы
    max_index = len(paginator.page_range)  # общее количество страниц

    start_index = index - 4 if index - 4 >= 0 else 0
    end_index = index + 5 if index + 5 < max_index else max_index

    page_range = paginator.page_range[start_index:end_index]
    
    form = ContactForm()
    return render(request, 'address_book/index.html', {
        'form': form, 
        'page_obj': page_obj, 
        'page_range': page_range
        })


@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('address_book:index_address_book') 
    else:
        form = ContactForm()
    return render(request, 'address_book/create_contact.html', {'form': form})

@login_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('address_book:index_address_book')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'address_book/edit_contact.html', {'form': form, 'contact': contact})

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user).order_by('id')  # Добавлено упорядочение
    paginator = Paginator(contacts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'address_book/all_contacts.html', {'page_obj': page_obj})

@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    data = {
        'id': contact.id,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'email': contact.email,
        'phone': contact.phone,
        'address': contact.address,
        'birth_date': contact.birth_date.strftime('%Y-%m-%d') if contact.birth_date else None,
    }
    return JsonResponse(data)

@login_required
def upcoming_birthdays(request):
    today = date.today()
    end_date = today + timedelta(days=10)
    
    # Фильтруем контакты, у которых день рождения в ближайшие 10 дней
    contacts = Contact.objects.filter(
        user=request.user, 
        birth_date__isnull=False
    ).filter(
        Q(
            Q(birth_date__month=today.month, birth_date__day__gte=today.day) |
            Q(birth_date__month=end_date.month, birth_date__day__lte=end_date.day)
        ) |
        Q(
            birth_date__month__gt=today.month, 
            birth_date__month__lt=end_date.month
        )
    )
    
    return render(request, 'address_book/upcoming_birthdays.html', {'contacts': contacts})

@login_required
def search_contacts(request):
    query = request.GET.get('q', '').strip()
    print(f"Search query: {query}")
    if ' ' in query:
        first_name, last_name = query.split(' ', 1)
        print(f"First name: {first_name}, Last name: {last_name}")
        contacts = Contact.objects.filter(
            Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name),
            user=request.user
        )[:10]
    else:
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query),
            user=request.user
        )[:10]
    results = [{'id': contact.id, 'name': f"{contact.first_name} {contact.last_name}"} for contact in contacts]
    print(f"Results: {results}")
    return JsonResponse(results, safe=False)

@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('address_book:index_address_book')
    return render(request, 'address_book/contact_confirm_delete.html', {'contact': contact})

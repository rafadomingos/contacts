from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.db.models import Q
from django.core.paginator import Paginator

def index(request):
    contacts = Contact.objects\
        .filter(show=True, owner=request.user)\
        .order_by('-id')
    
    paginator = Paginator(contacts, 10) 
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    # print(contacts.query)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contact List',
    }

    return render(
        request, 
        'contact/index.html',
        context
        )

def contact(request, contact_id):
    single_contact = get_object_or_404(
        Contact.objects.filter(pk=contact_id, show=True, owner=request.user)
    )
    
    site_title = f'{single_contact.first_name} {single_contact.last_name}'

    context = {
        'contact': single_contact,
        'site_title': site_title,
    }

    return render(
        request, 
        'contact/contact.html',
        context
        )

def search(request):
    # Busca pelo parametro, caso nao encontrar carrega espaço, 
    # strip é para tirar espaço em branco do inicio e final da string
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')

    contacts = Contact.objects\
        .filter(show=True, owner=request.user)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(description__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value) 
            )\
        .order_by('-id')
    
    paginator = Paginator(contacts, 10) 
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contact List',
    }

    return render(
        request, 
        'contact/index.html',
        context
        )
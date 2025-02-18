from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from contact.forms import ContactForm
from contact.models import Contact

@login_required(login_url='contact:login')
def create(request):

    form_action = reverse('contact:create')

    if request.method == 'POST':

        form = ContactForm(request.POST, request.FILES)

        context = {
        'form': form,
        'site_title': 'Contact Create',
        'form_action': form_action,
        }

        if form.is_valid():
            # Se utilizar o commit=False, o objeto não é salvo no banco de dados, 
            # mas é retornado para que você possa fazer algo com ele antes de salvar.
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()

            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request, 
            'contact/create.html',
            context
            )


    context = {
        'form': ContactForm(),
        'site_title': 'Contact Create',
        'form_action': form_action,
    }

    return render(
        request, 
        'contact/create.html',
        context
        )

@login_required(login_url='contact:login')
def update(request, contact_id):
    form_action = reverse('contact:update', args=(contact_id,))
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)

    if request.method == 'POST':

        form = ContactForm(request.POST, request.FILES, instance=contact)

        context = {
        'form': form,
        'site_title': 'Contact Create',
        'form_action': form_action,
        }

        if form.is_valid():
            # Se utilizar o commit=False, o objeto não é salvo no banco de dados, 
            # mas é retornado para que você possa fazer algo com ele antes de salvar.
            contact = form.save(commit=False)
            contact.show = True
            contact.save()

            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request, 
            'contact/create.html',
            context
            )


    context = {
        'form': ContactForm(instance=contact),
        'site_title': 'Contact Create',
        'form_action': form_action,
    }

    return render(
        request, 
        'contact/create.html',
        context
        )

@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)

    confirmation = request.POST.get('confirmation', 'no')
    print(confirmation)
    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(
            request, 
            'contact/contact.html',
            {
                'contact': contact,
                'site_title': 'Contact Delete Confirmation',
                'confirmation' : confirmation,
            }
            )
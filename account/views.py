from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.template.loader import get_template

from .forms import LoginForm, UserRegisterationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import UpdateUserForm, UpdateProfileForm
from django.views.generic import ListView

from .utils import render_to_pdf


def home(request):
    return render(request, 'base.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authenticated successfully')
                    return dashboard(request)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login <a href="http://localhost:8000/login/"> login </a>')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegisterationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('/account/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def client_list(request):
    client = Client.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/client_list.html', {'client': client})


def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        # update
        form = ClientForms(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.updated_date = timezone.now()
            client.save()
            client = Client.objects.filter(created_date__lte=timezone.now())
        return render(request, 'crm/client_list.html', {'client': client})
    else:
        # edit
        form = ClientForms(instance=client)
    return render(request, 'crm/client_edit.html', {'form': form})


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('/client_list')

def client_orders(request, pk):
    orders = Order.objects.all()
    clientid = ""
    order = []
    for ordr in orders:
        if ordr.client_id == pk:
            order.append(ordr)
            clientid = ordr.client_id
    print('ordr is', clientid)
    return render(request, 'crm/client_orders.html', {'order': order, 'clientId': clientid})



def inventory_list(request):
    inventory = Inventory.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/inventory_list.html', {'inventory': inventory})


def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        # update
        form = InventoryForms(request.POST, instance=Inventory)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.updated_date = timezone.now()
            inventory.save()
            inventory = Inventory.objects.filter(created_date__lte=timezone.now())
        return render(request, 'crm/inventory_list.html', {'inventory': inventory})
    else:
        # edit
        form = InventoryForms(instance=inventory)
    return render(request, 'crm/inventory_edit.html', {'form': form})


def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    return redirect('/inventory_list')


def order_list(request):
    order = Order.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/order_list.html', {'order': order})


def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    visit = get_object_or_404(Visit, pk=order.date.pk)
    if request.method == "POST":
        # update
        form = OrdereditForms(request.POST, instance=order)
        visitForm = VisitForms(request.POST, instance=visit)
        if form.is_valid():
            order = form.save(commit=False)
            visit = visitForm.save(commit=False)
            order.updated_date = timezone.now()
            order.save()
            visit.save()
            order = Order.objects.filter(created_date__lte=timezone.now())
        return render(request, 'crm/order_list.html', {'order': order})
    else:
        # edit
        form = OrdereditForms(instance=order)
        visitForm = VisitForms(instance=visit)
    return render(request, 'crm/order_edit.html', {'form': form, 'visitForm':visitForm})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('/order_list')


@login_required
def client_new(request):
    if request.method == "POST":
        form = ClientForms(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_date = timezone.now()
            client.save()
            client = Client.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/client_list.html',
                          {'client': client})
    else:
        form = ClientForms()
        # print("Else")
    return render(request, 'crm/client_new.html', {'form': form})

@login_required
def order_new(request, pk):
    if request.method == "POST":
        form = OrderForms(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_date = timezone.now()
            order.save()
            order = Order.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/order_list.html',
                          {'order': order})
    else:
        form = OrderForms()
        print("Else", form.fields['client'])
        form.fields['client'].initial = pk
    return render(request, 'crm/order_new.html', {'form': form})


def client_search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        clients = Client.objects.filter(first_name__contains=searched)
        # if 'searched' in request.GET:
        #     clients = list()
        #     for client in clients:
        #         clients.append(client.first_name)
        #     return JsonResponse(clients, safe=False)
        return render(request, 'crm/client_search.html', {'searched': searched, 'clients': clients})
    else:
        return render(request, 'crm/client_search.html', {})
def download_orderReport(request, pk):
    order = get_object_or_404(Order, pk=pk)
    template = get_template('crm/print_order_details.html')
    context = {'form': order}
    html = template.render(context)
    pdf = render_to_pdf('crm/print_order_details.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "order_details.pdf"
        content = "inline; filename='%s'" % filename
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def download_allorderReport(request):
    order = Order.objects.filter(created_date__lte=timezone.now())
    template = get_template('crm/print_orders.html')
    context = {'order': order}
    html = template.render(context)
    pdf = render_to_pdf('crm/print_orders.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "print_orders.html.pdf"
        content = "inline; filename='%s'" % filename
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

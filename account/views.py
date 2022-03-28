from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegisterationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect


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
    return render(request, 'base.html', {'section': 'dashboard'})


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
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
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
    return redirect('crm/client_list')


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
    return redirect('crm/inventory_list')


def order_list(request):
    order = Order.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/order_list.html', {'order': order})


def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        # update
        form = OrderForms(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.updated_date = timezone.now()
            order.save()
            order = Order.objects.filter(created_date__lte=timezone.now())
        return render(request, 'crm/order_list.html', {'order': order})
    else:
        # edit
        form = ClientForms(instance=order)
    return render(request, 'crm/order_edit.html', {'form': form})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('crm/order_list')


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

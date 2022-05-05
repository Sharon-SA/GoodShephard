from datetime import timezone, datetime, timedelta

import xlwt
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.urls import reverse

from .forms import LoginForm, UserRegisterationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import UpdateUserForm, UpdateProfileForm
from django.views.generic import ListView

from .utils import render_to_pdf


class ClientVisitsModelObject:
    clientID: int = 0
    client_first_name: str
    client_last_name: str
    firstdateTime: datetime
    lastdateTime: datetime
    numberofVisits: int = 0

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
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('/account/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user)
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
    print("pk is", pk)
    orders = Order.objects.all()
    clientid = ""
    order = []
    for ordr in orders:
        if ordr.client_id == pk:
            order.append(ordr)
            clientid = ordr.client_id
    if clientid == "":
        clientid = pk
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
    visit = get_object_or_404(Visit, pk=order.client.pk)

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
    return render(request, 'crm/order_edit.html', {'form': form, 'visitForm': visitForm})


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
        form = NewOrderForm(request.POST)
        visit_form = VisitForms(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            visit = visit_form.save(commit=False)
            order.created_date = timezone.now()
            visit.created_date = timezone.now()
            visit.client = order.client
            visit.save()
            order.visit = visit
            order.save()
            order = Order.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/order_list.html',
                          {'order': order})
    else:
        form = NewOrderForm()
        visitForm = VisitForms()
        print("Else", form.fields['client'])
        form.fields['client'].initial = pk
    return render(request, 'crm/order_new.html', {'form': form, 'visitForm': visitForm})


def client_search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        clients = Client.objects.filter(first_name__contains=searched)
        # if 'searched' in request.GET:
        #     clients = list()
        #     for client in clients:
        #         clients.append(client.first_name)
        #     return JsonResponse(clients, safe=False)
        print("a")
        return render(request, 'crm/client_search.html', {'searched': searched, 'clients': clients})
    else:
        print("b")
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


def viewReport(request):


    return render(request, 'reports/reports_list.html')


def client_visits_report(request):
    clientVisits = Visit.objects.all()

    clientVisitsDataList = build_client_visits_list_from_clientVisits(clientVisits)
    return render(request, 'reports/client_visits.html', {'data_list': clientVisitsDataList})


def client_orders_fulfilled(request):
    order = Order.objects.filter(created_date__lte=timezone.now())
    return render(request, 'reports/fulfillment_report.html', {'data_list': order})


def build_client_visits_list_from_clientVisits(clientVisits):
    clientVisitsDataList = []
    for clientVisit in clientVisits:
        clientVisitsModelObject: ClientVisitsModelObject = None

        for data in clientVisitsDataList:
            if data.clientID == clientVisit.client.pk:
                clientVisitsModelObject = data
                break

        if clientVisitsModelObject == None:
            clientVisitsModelObject = ClientVisitsModelObject()
            clientVisitsModelObject.clientID = clientVisit.client.pk
            clientVisitsModelObject.client_first_name = clientVisit.client.first_name
            clientVisitsModelObject.client_last_name = clientVisit.client.last_name
            clientVisitsModelObject.firstdateTime = clientVisit.created_date
            clientVisitsModelObject.lastdateTime = clientVisit.created_date
            clientVisitsModelObject.firstdateTime = clientVisitsModelObject.firstdateTime.replace(tzinfo=timezone.utc)
            clientVisitsModelObject.lastdateTime = clientVisitsModelObject.lastdateTime.replace(tzinfo=timezone.utc)
            clientVisitsDataList.append(clientVisitsModelObject)

        clientVisitsModelObject.numberofVisits += 1

        if clientVisit.created_date < clientVisitsModelObject.firstdateTime:
            clientVisitsModelObject.firstdateTime = clientVisit.created_date
            clientVisitsModelObject.firstdateTime = clientVisitsModelObject.firstdateTime.replace(tzinfo=timezone.utc)

        if clientVisit.created_date > clientVisitsModelObject.lastdateTime:
            clientVisitsModelObject.lastdateTime = clientVisit.created_date
            clientVisitsModelObject.lastdateTime = clientVisitsModelObject.lastdateTime.replace(tzinfo=timezone.utc)

    return clientVisitsDataList


def export_client_visits_report_csv(request: HttpRequest):
    client_visits_data = Visit.objects.all()
    if client_visits_data.__len__() == 0:
        url = (
            "{}?".format(reverse("client_visits_report")))
        messages.error(request, "Could not export excel sheet with given parameters.")
        response = HttpResponseRedirect(url)
        return response

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="client_visits_report.xls"'

    workbook = xlwt.Workbook(encoding="utf-8")

    # adding sheet
    worksheet = workbook.add_sheet("Report")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = [
        "Client Id",
        "First name",
        "Last name",
        "First visit datetime",
        "Last visit datetime",
        "Number of visits",
    ]

    # write column headers in sheet
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = "dd/mm/yyyy HH:MM"

    # get your data, from database or from a text file...
    data_list: list[ClientVisitsModelObject] = build_client_visits_list_from_clientVisits(client_visits_data)
    for data in data_list:
        data.firstdateTime = data.firstdateTime.replace(tzinfo=None)
        data.firstdateTime = data.firstdateTime - timedelta(hours=5, minutes=00)
        data.lastdateTime = data.lastdateTime.replace(tzinfo=None)
        data.lastdateTime = data.lastdateTime - timedelta(hours=5, minutes=00)
        row_num = row_num + 1
        test = vars(data)
        columns = [test[key] for key in test]
        for col_num in range(len(columns)):
            # For row three and four which are date times use date format
            worksheet.write(
                row_num,
                col_num,
                columns[col_num],
                font_style if col_num != 3 and col_num != 4 else date_format,
            )

    workbook.save(response)
    return response


def export_orders_list_report_csv(request: HttpRequest):
    orders_data = Order.objects.all()
    if orders_data.__len__() == 0:
        url = (
            "{}?".format(reverse("orders_report")))
        messages.error(request, "Could not export excel sheet with given parameters.")
        response = HttpResponseRedirect(url)
        return response

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="orders_report.xls"'

    workbook = xlwt.Workbook(encoding="utf-8")

    # adding sheet
    worksheet = workbook.add_sheet("Report")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = [
        "Client Name",
        "Item Description",
        "Requested Quantity",
        "Delivered Quantity",
        "Date Entered",
    ]

    # write column headers in sheet
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = "dd/mm/yyyy HH:MM"

    # get your data, from database or from a text file...
    col_num = 0
    for data in orders_data:
        data.date = data.date.replace(tzinfo=None)
        data.date = data.date - timedelta(hours=5, minutes=00)
        row_num = row_num + 1
        worksheet.write(row_num, col_num, data.client.first_name)
        worksheet.write(row_num, col_num+1, data.item_description.item_description)
        worksheet.write(row_num, col_num+2, data.request_quantity)
        worksheet.write(row_num, col_num + 3, data.delivered_quantity)
        worksheet.write(row_num, col_num + 4, data.date, date_format)

    workbook.save(response)
    return response


def inventory_report(request):
    data_list = Inventory.objects.all()
    return render(request,'reports/inventory_report.html',{'data_list':data_list})


def export_inventory_list_report_csv(request):
    inv_data = Inventory.objects.all()
    if inv_data.__len__() == 0:
        url = (
            "{}?".format(reverse("orders_report")))
        messages.error(request, "Could not export excel sheet with given parameters.")
        response = HttpResponseRedirect(url)
        return response

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="inventory_report.xls"'

    workbook = xlwt.Workbook(encoding="utf-8")

    # adding sheet
    worksheet = workbook.add_sheet("Report")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = [
        "UPS Code",
        "Item Description",
        "Total Quantity",
    ]

    # write column headers in sheet
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = "dd/mm/yyyy HH:MM"

    # get your data, from database or from a text file...
    col_num = 0
    for data in inv_data:
        row_num = row_num + 1
        worksheet.write(row_num, col_num, data.UPScode)
        worksheet.write(row_num, col_num + 1, data.item_description)
        worksheet.write(row_num, col_num + 2, data.total_quantity)


    workbook.save(response)
    return response
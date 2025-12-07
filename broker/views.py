from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import Farmer, MilkCollection
from .forms import FarmerForm, MilkCollectionForm
import requests


def send_sms(phone_number, message):
    """
    Send SMS using Twilio Messaging Service (better for international)
    """
    try:
        # Normalize phone number
        if phone_number.startswith('0'):
            phone_number = '+254' + phone_number[1:]
        elif not phone_number.startswith('+'):
            phone_number = '+254' + phone_number

        from twilio.rest import Client
        from django.conf import settings

        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        messaging_service_sid = settings.TWILIO_MESSAGING_SERVICE_SID  # New!

        client = Client(account_sid, auth_token)

        # Use messaging_service_sid instead of from_
        message_obj = client.messages.create(
            body=message,
            messaging_service_sid=messaging_service_sid,  # Changed!
            to=phone_number
        )

        print(f"SMS sent successfully! SID: {message_obj.sid}")
        return True

    except Exception as e:
        print(f"SMS Error: {e}")
        return False


def dashboard(request):
    total_farmers = Farmer.objects.filter(is_active=True).count()
    today = timezone.now().date()
    today_collections = MilkCollection.objects.filter(collection_date=today)
    today_quantity = today_collections.aggregate(Sum('quantity'))['quantity__sum'] or 0
    today_revenue = today_collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Monthly stats
    month_start = today.replace(day=1)
    month_collections = MilkCollection.objects.filter(collection_date__gte=month_start)
    month_quantity = month_collections.aggregate(Sum('quantity'))['quantity__sum'] or 0
    month_revenue = month_collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    recent_collections = MilkCollection.objects.all()[:10]
    top_farmers = Farmer.objects.annotate(
        total_milk=Sum('collections__quantity')
    ).order_by('-total_milk')[:5]

    context = {
        'total_farmers': total_farmers,
        'today_quantity': today_quantity,
        'today_revenue': today_revenue,
        'month_quantity': month_quantity,
        'month_revenue': month_revenue,
        'recent_collections': recent_collections,
        'top_farmers': top_farmers,
    }
    return render(request, 'dashboard.html', context)


def farmer_list(request):
    query = request.GET.get('q')
    farmers = Farmer.objects.all()

    if query:
        farmers = farmers.filter(
            Q(farmer_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(location__icontains=query)
        )

    context = {'farmers': farmers, 'query': query}
    return render(request, 'farmer_list.html', context)


def farmer_detail(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    collections = farmer.collections.all()[:20]

    total_collected = farmer.get_total_milk_collected()
    month_collected = farmer.get_collections_this_month()
    total_revenue = collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        'farmer': farmer,
        'collections': collections,
        'total_collected': total_collected,
        'month_collected': month_collected,
        'total_revenue': total_revenue,
    }
    return render(request, 'farmer_detail.html', context)


def farmer_create(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            farmer = form.save()
            messages.success(request, f'Farmer {farmer.farmer_id} registered successfully!')
            return redirect('farmer_detail', pk=farmer.pk)
    else:
        form = FarmerForm()

    return render(request, 'farmer_form.html', {'form': form, 'title': 'Register New Farmer'})


def farmer_update(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer details updated successfully!')
            return redirect('farmer_detail', pk=farmer.pk)
    else:
        form = FarmerForm(instance=farmer)

    return render(request, 'farmer_form.html', {'form': form, 'title': 'Update Farmer Details'})


def farmer_delete(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        farmer.is_active = False
        farmer.save()
        messages.success(request, 'Farmer deactivated successfully!')
        return redirect('farmer_list')

    return render(request, 'farmer_confirm_delete.html', {'farmer': farmer})


def collection_create(request):
    if request.method == 'POST':
        form = MilkCollectionForm(request.POST)
        if form.is_valid():
            collection = form.save()

            # Send SMS notification
            farmer = collection.farmer
            message = (
                f"Dear {farmer.first_name}, "
                f"we have received {collection.quantity}L of milk from you today ({collection.collection_date}). "
                f"Total amount: KES {collection.total_amount}. Thank you!"
            )

            sms_status = send_sms(farmer.phone_number, message)
            collection.sms_sent = sms_status
            collection.save()

            if sms_status:
                messages.success(request, f'Collection recorded and SMS sent to {farmer.first_name}!')
            else:
                messages.warning(request, f'Collection recorded but SMS failed to send.')

            return redirect('dashboard')
    else:
        form = MilkCollectionForm()

    return render(request, 'collection_form.html', {'form': form})


def collection_history(request):
    collections = MilkCollection.objects.all()

    # Filters
    farmer_id = request.GET.get('farmer')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if farmer_id:
        collections = collections.filter(farmer_id=farmer_id)
    if date_from:
        collections = collections.filter(collection_date__gte=date_from)
    if date_to:
        collections = collections.filter(collection_date__lte=date_to)

    total_quantity = collections.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_revenue = collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        'collections': collections,
        'total_quantity': total_quantity,
        'total_revenue': total_revenue,
        'farmers': Farmer.objects.filter(is_active=True),
    }
    return render(request, 'collection_history.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Room, Customer, CheckIn
from django.utils import timezone

def dashboard(request):
    rooms = Room.objects.select_related('room_type').all().order_by('room_number')
    return render(request, 'index.html', {'rooms': rooms})

@csrf_exempt
def checkin(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    if request.method == 'POST':
        # 模擬一位客戶入住（簡化處理，實際可改為表單輸入）
        customer, created = Customer.objects.get_or_create(
            national_id='DUMMY1234',
            defaults={'name': '測試客戶', 'phone': '0912345678'}
        )
        CheckIn.objects.create(
            customer=customer,
            room=room,
            guest_count=1,
            checkin_time=timezone.now(),
            checkout_time=timezone.now()  # 可在退房時更新
        )
        room.status = '使用中'
        room.save()
        return redirect('dashboard')

@csrf_exempt
def checkout(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    if request.method == 'POST':
        checkin_record = CheckIn.objects.filter(room=room, checkout_time__lte=timezone.now()).last()
        if checkin_record:
            checkin_record.checkout_time = timezone.now()
            checkin_record.save()
        room.status = '空房'
        room.save()
        return redirect('dashboard')
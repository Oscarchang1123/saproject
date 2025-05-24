import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SAProject.settings')
django.setup()

from hotelapp.models import RoomType, Room

rt, created = RoomType.objects.get_or_create(code='A1', defaults={'name': '標準雙人房'})

rooms_data = [
    {'room_number': '101', 'price': 2000},
    {'room_number': '102', 'price': 2200},
    {'room_number': '103', 'price': 2500},
]

for data in rooms_data:
    room, created = Room.objects.get_or_create(
        room_number=data['room_number'],
        defaults={
            'room_type': rt,
            'price': data['price'],
            'status': '空房'
        }
    )
    if created:
        print(f"新增房間 {room.room_number}")
    else:
        print(f"房間 {room.room_number} 已存在")

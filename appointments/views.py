# appointments/views.py

from django.shortcuts import render

def index(request):
    context = {
        'range_list': range(1, 5)  # 將 range(1, 5) 傳遞給模板
    }
    return render(request, 'index.html', context)

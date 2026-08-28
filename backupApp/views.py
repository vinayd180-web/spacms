from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.core.management import call_command
import json
import os
from django.conf import settings

@staff_member_required
def backup_data(request):
    if request.method == 'POST':
        # Database backup
        import subprocess
        import datetime
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'backup_{timestamp}.json'
        filepath = os.path.join(settings.BASE_DIR, filename)
        
        # Dump data
        with open(filepath, 'w') as f:
            call_command('dumpdata', stdout=f)
        
        # Send file
        with open(filepath, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    
    return render(request, 'backupApp/backup.html')

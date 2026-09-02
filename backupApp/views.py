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

@staff_member_required
def restore_data(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        import json
        from django.core.management import call_command
        file = request.FILES['backup_file']
        data = json.loads(file.read().decode('utf-8'))
        call_command('loaddata', file.temporary_file_path() if hasattr(file, 'temporary_file_path') else None)
        messages.success(request, "Data restored successfully!")
        return redirect('restore_data')
    return render(request, 'backupApp/restore.html')

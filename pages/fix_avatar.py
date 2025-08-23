from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings') 
application = get_wsgi_application()

from pages.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    user = User.objects.get(username='locoabreu2010')
    profile = Profile.objects.get(user=user)
    profile.avatar = None
    profile.save()
    print("✅ Avatar eliminado correctamente.")
except Exception as e:
    print(f"❌ Error: {e}")

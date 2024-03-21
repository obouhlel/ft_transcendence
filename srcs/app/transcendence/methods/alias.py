from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from transcendence.models import CustomUser
import json
import logging

logger = logging.getLogger(__name__)

@require_http_methods(['POST'])
def postAlias(request):
    try:
        data = json.loads(request.body)
        alias = data['alias']
        if not alias or alias == '':
            user = CustomUser.objects.get(username=request.user.username)
            user.alias = ''
            user.save()
            return JsonResponse({'status': 'ok', 'message': 'Alias removed.'})
        if CustomUser.objects.filter(alias=alias).exists():
            return JsonResponse({'status': 'error', 'message': 'Alias already exists.'}, status=400)
        user = CustomUser.objects.get(username=request.user.username)
        user.alias = alias
        user.save()
        return JsonResponse({'status': 'ok', 'message': 'Alias updated.'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User does not exist.'}, status=404)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Propiedad, Ubicacion

@receiver(post_delete, sender=Propiedad)
def delete_ubicacion_on_propiedad_delete(sender, instance, **kwargs):
    if instance.ubicacion:
        instance.ubicacion.delete()

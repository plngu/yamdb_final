from rest_framework import viewsets

from .permissions import AllOrRead, ReadOnly


class CreateUpdateDestroyMixin(viewsets.ModelViewSet):
    permission_classes = [AllOrRead, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(), )
        return super().get_permissions()

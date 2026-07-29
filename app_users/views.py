from mailbox import Message

from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Notification, Profil
from .serializers import MessageSerializer, NotificationSerializer, ProfilSerializer, InscriptionSerializer, UserSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Profil
from .serializers import ProfilSerializer, InscriptionSerializer, UserSerializer

class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Profil.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return InscriptionSerializer 
        return ProfilSerializer  

    def create(self, request, *args, **kwargs):
        # On utilise InscriptionSerializer pour valider et créer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profil = serializer.save()

        # On utilise ProfilSerializer pour renvoyer la réponse
        read_serializer = ProfilSerializer(profil)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
# ViewSet pour le profil de l'utilisateur connecté
class MonProfilViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtre pour ne renvoyer que le profil de l'utilisateur actuellement connecté
        return Profil.objects.filter(user=self.request.user)

    def get_object(self):
        # Retourne directement le profil de l'utilisateur connecté sans passer par un ID
        return self.request.user.profil

class ModifierUtilisateurView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        # Récupère l'utilisateur connecté
        user = request.user
        
        # On utilise le sérialiseur UserSerializer pour valider et modifier
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(destinataire=self.request.user).order_by('-dateEnvoi')

    def create(self, request, *args, **kwargs):
        data = request.data
        destinataire_id = data.get('destinataire_id')
        contenu = data.get('contenu')

        if not destinataire_id or not contenu:
            return Response(
                {"error": "destinataire_id et contenu sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            destinataire = User.objects.get(id=destinataire_id)
        except User.DoesNotExist:
            return Response({"error": "Destinataire introuvable"}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            expediteur=request.user,
            destinataire=destinataire,
            contenu=contenu
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)



class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user).order_by('-dateEnvoi')

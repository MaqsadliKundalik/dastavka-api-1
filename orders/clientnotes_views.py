from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from .models import ClientNotes, Client
from .serializers import ClientNotesSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Barcha ClientNotes ro'yxati",
        description="Tizimda mavjud barcha ClientNotes yozuvlarini ko'rish.",
        tags=["ClientNotes"]
    ),
    create=extend_schema(
        summary="Yangi ClientNotes yaratish",
        description="Yangi ClientNotes yozuvini yaratish.",
        request=ClientNotesSerializer,
        responses={
            201: ClientNotesSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar")
        },
        examples=[
            OpenApiExample(
                name='ClientNotes yaratish',
                value={
                    "client_id": 1,
                    "baklashka_soni": 10,
                    "arenda_soni": 5,
                    "kuler_soni": 2,
                    "pompa_soni": 1
                }
            )
        ],
        tags=["ClientNotes"]
    )
)
class ClientNotesListCreateView(generics.ListCreateAPIView):
    """
    ClientNotes ro'yxati va yangi ClientNotes yaratish
    """
    queryset = ClientNotes.objects.all()
    serializer_class = ClientNotesSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    retrieve=extend_schema(
        summary="ClientNotes ma'lumotlarini ko'rish",
        description="ID bo'yicha bitta ClientNotes ma'lumotlarini ko'rish",
        tags=["ClientNotes"]
    ),
    update=extend_schema(
        summary="ClientNotes ma'lumotlarini yangilash",
        description="ClientNotes ma'lumotlarini to'liq yangilash (PUT)",
        request=ClientNotesSerializer,
        responses={
            200: ClientNotesSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar"),
            404: OpenApiResponse(description="ClientNotes topilmadi")
        },
        tags=["ClientNotes"]
    ),
    partial_update=extend_schema(
        summary="ClientNotes ma'lumotlarini qisman yangilash",
        description="ClientNotes ma'lumotlarini qisman yangilash (PATCH)",
        request=ClientNotesSerializer,
        responses={
            200: ClientNotesSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar"),
            404: OpenApiResponse(description="ClientNotes topilmadi")
        },
        tags=["ClientNotes"]
    ),
    destroy=extend_schema(
        summary="ClientNotes o'chirish",
        description="ClientNotes yozuvini o'chirish",
        responses={
            204: OpenApiResponse(description="Muvaffaqiyatli o'chirildi"),
            404: OpenApiResponse(description="ClientNotes topilmadi")
        },
        tags=["ClientNotes"]
    )
)
class ClientNotesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Bitta ClientNotes bilan bog'liq CRUD operatsiyalar
    """
    queryset = ClientNotes.objects.all()
    serializer_class = ClientNotesSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    summary="Mijoz uchun ClientNotes",
    description="Berilgan mijoz ID si uchun barcha ClientNotes yozuvlarini ko'rish",
    responses={
        200: ClientNotesSerializer(many=True),
        404: OpenApiResponse(description="Mijoz topilmadi")
    },
    tags=["ClientNotes"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def client_notes_by_client(request, client_id):
    """
    Muayyan mijoz uchun ClientNotes yozuvlari
    """
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response(
            {"error": f"ID={client_id} bo'lgan mijoz topilmadi!"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    notes = ClientNotes.objects.filter(client=client)
    serializer = ClientNotesSerializer(notes, many=True)
    
    return Response({
        "client_id": client.id,
        "client_name": client.full_name,
        "notes_count": notes.count(),
        "notes": serializer.data
    }, status=status.HTTP_200_OK)

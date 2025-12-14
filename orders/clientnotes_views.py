from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import ClientNotes, Client
from .serializers import ClientNotesSerializer


@extend_schema(
    summary="Mijoz uchun ClientNotes olish",
    description="Client ID orqali uning notes obyektini olish",
    parameters=[OpenApiParameter(name='client_id', type=int, location=OpenApiParameter.PATH, description='Client ID')],
    responses={
        200: ClientNotesSerializer,
        404: OpenApiResponse(description="Client yoki ClientNotes topilmadi")
    },
    tags=["ClientNotes"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_client_notes(request, client_id):
    """
    Client ID orqali uning notes obyektini olish
    """
    client = get_object_or_404(Client, id=client_id)
    try:
        notes = ClientNotes.objects.get(client=client)
        serializer = ClientNotesSerializer(notes)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ClientNotes.DoesNotExist:
        return Response(
            {"error": f"ID={client_id} bo'lgan client uchun notes topilmadi!"},
            status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(
    summary="Mijoz uchun ClientNotes yaratish yoki yangilash",
    description="Client ID orqali uning notes obyektini yaratish yoki yangilash",
    parameters=[OpenApiParameter(name='client_id', type=int, location=OpenApiParameter.PATH, description='Client ID')],
    request=ClientNotesSerializer,
    responses={
        200: ClientNotesSerializer,
        201: ClientNotesSerializer,
        400: OpenApiResponse(description="Noto'g'ri ma'lumotlar"),
        404: OpenApiResponse(description="Client topilmadi")
    },
    tags=["ClientNotes"]
)
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.AllowAny])
def update_client_notes(request, client_id):
    """
    Client ID orqali uning notes obyektini yangilash (PUT/PATCH)
    """
    client = get_object_or_404(Client, id=client_id)
    
    try:
        notes = ClientNotes.objects.get(client=client)
        serializer = ClientNotesSerializer(notes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ClientNotes.DoesNotExist:
        # Agar notes mavjud bo'lmasa, yangi yaratamiz
        serializer = ClientNotesSerializer(data={**request.data, 'client_id': client_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Mijoz uchun ClientNotes o'chirish",
    description="Client ID orqali uning notes obyektini o'chirish",
    parameters=[OpenApiParameter(name='client_id', type=int, location=OpenApiParameter.PATH, description='Client ID')],
    responses={
        204: OpenApiResponse(description="Muvaffaqiyatli o'chirildi"),
        404: OpenApiResponse(description="Client yoki ClientNotes topilmadi")
    },
    tags=["ClientNotes"]
)
@api_view(['DELETE'])
@permission_classes([permissions.AllowAny])
def delete_client_notes(request, client_id):
    """
    Client ID orqali uning notes obyektini o'chirish
    """
    client = get_object_or_404(Client, id=client_id)
    
    try:
        notes = ClientNotes.objects.get(client=client)
        notes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ClientNotes.DoesNotExist:
        return Response(
            {"error": f"ID={client_id} bo'lgan client uchun notes topilmadi!"},
            status=status.HTTP_404_NOT_FOUND
        )

from rest_framework import viewsets, generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from transaction.models import Transaction
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["title", "author", "isbn"]
    search_fields = ["title", "author", "isbn"]

    def get_queryset(self):
        queryset = super().get_queryset()
        available = self.request.query_params.get("available", None)
        if available is not None:
            if available.lower() == "true":
                queryset = queryset.filter(copies_available__gt=0)
            elif available.lower() == "false":
                queryset = queryset.filter(copies_available=0)
        return queryset


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def checkout(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        if book.copies_available > 0:
            book.copies_available -= 1
            book.save()
            transaction = Transaction.objects.create(user=request.user, book=book)
            return Response(
                {"status": "book checked out", "transaction_id": transaction.id}
            )
        return Response({"status": "no copies available"}, status=400)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        book = transaction.book
        book.copies_available += 1
        book.save()
        transaction.return_date = timezone.now()
        transaction.save()
        return Response({"status": "book returned"})

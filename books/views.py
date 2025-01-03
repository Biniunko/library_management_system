from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from transaction.models import Transaction
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


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

import logging
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from books.models import Book
from subscription.models import Subscription

logger = logging.getLogger(__name__)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class CheckOutBookView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(pk=request.data["book"])
        except Book.DoesNotExist:
            logger.error("Book not found")
            return Response({"error": "Book not found"}, status=404)

        user = request.user
        try:
            subscription = Subscription.objects.get(user=user)
            if not subscription.active:
                logger.error("Subscription inactive")
                return Response({"error": "Subscription inactive"}, status=403)
        except Subscription.DoesNotExist:
            logger.error("No subscription found")
            return Response({"error": "No subscription found"}, status=403)

        if book.copies_available > 0:
            book.copies_available -= 1
            book.save()
            transaction = Transaction.objects.create(user=user, book=book)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        logger.error("No copies available")
        return Response({"error": "No copies available"}, status=400)

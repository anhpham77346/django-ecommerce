from django.shortcuts import render
from book.models import Book
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from bson import ObjectId
from .api_clients import get_book_by_id
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

@login_required(login_url='/account/login')
def cart_view(request):
    """Lấy giỏ hàng của người dùng hiện tại và hiển thị trên giao diện."""
    try:
        # Lấy giỏ hàng của user từ MySQL
        cart = Cart.objects.using('cart_db').filter(customer_id=request.user.id).first()

        if not cart:
            return render(request, "cart/cart.html", {"cart_items": [], "total_price": 0})

        # Lấy các mục giỏ hàng từ MySQL
        cart_items = CartItem.objects.using('cart_db').filter(cart=cart)

        total_price = 0

        # Thêm thông tin sách từ MongoDB vào mỗi mục giỏ hàng
        for item in cart_items:
            book = get_book_by_id(item.book_id)

            if book:
                item.book_title = book["title"]
                item.book_author = book["author"]
                item.book_price = book["price"]
                item.book_url = book["image_url"]
            else:
                item.book_title = "Không tìm thấy"
                item.book_author = "Không rõ"
                item.book_price = 0

            # Tính tổng tiền từng sản phẩm và tổng tiền giỏ hàng
            item.total_price_per_item = item.quantity * item.book_price
            total_price += item.total_price_per_item

        return render(request, "cart/cart.html", {
            "cart_items": cart_items,
            "total_price": total_price
        })

    except Exception as e:
        return render(request, "cart/cart.html", {"error": str(e)})

class AddToCartView(APIView):
    def post(self, request, book_id):
        # Kiểm tra người dùng đã đăng nhập chưa
        if not request.user.is_authenticated:
            return Response({"error": "Bạn cần đăng nhập."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Lấy thông tin sách từ API
            book = get_book_by_id(book_id)

            if not book:
                return Response({"error": "Sách không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

            # Tìm hoặc tạo giỏ hàng của người dùng
            cart, created = Cart.objects.using('cart_db').get_or_create(customer_id=request.user.id)

            # Thêm sách vào giỏ hàng
            cart_item, created = CartItem.objects.using('cart_db').get_or_create(
                cart=cart,
                book_id=str(book["id"]),
                defaults={"quantity": 1, "price_at_purchase": book["price"]}
            )

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return Response(
                {"message": "Đã thêm vào giỏ hàng", "book": book["title"]},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RemoveFromCartView(APIView):
    def delete(self, request, item_id):
        # Kiểm tra người dùng đã đăng nhập chưa
        if not request.user.is_authenticated:
            return Response({"error": "Bạn cần đăng nhập."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Tìm giỏ hàng của người dùng
            cart = Cart.objects.using('cart_db').filter(customer_id=request.user.id).first()
            if not cart:
                return Response({"error": "Giỏ hàng trống."}, status=status.HTTP_404_NOT_FOUND)

            # Kiểm tra xem item có trong giỏ hàng không
            cart_item = CartItem.objects.using('cart_db').filter(cart=cart, id=item_id).first()
            if not cart_item:
                return Response({"error": "Sản phẩm không có trong giỏ hàng."}, status=status.HTTP_404_NOT_FOUND)

            # Xóa sản phẩm khỏi giỏ hàng
            cart_item.delete()

            return Response({"message": "Đã xóa sản phẩm khỏi giỏ hàng."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

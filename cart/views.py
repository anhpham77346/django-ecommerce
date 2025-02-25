from django.shortcuts import render, redirect
from django.http import JsonResponse
from book.models import Book
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from bson import ObjectId

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
            book = Book.objects(id=ObjectId(item.book_id)).first()
            if book:
                item.book_title = book.title
                item.book_author = book.author
                item.book_price = book.price
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

def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"error": "Bạn cần đăng nhập để thêm vào giỏ hàng."}, status=403)
        return redirect('login')

    try:
        book = Book.objects(id=ObjectId(book_id)).first()

        if not book:
            return JsonResponse({"error": "Sách không tồn tại."}, status=404)
        
        cart, created = Cart.objects.using('cart_db').get_or_create(customer_id=request.user.id)

        cart_item, created = CartItem.objects.using('cart_db').get_or_create(
            cart=cart,
            book_id=str(book.id),
            defaults={"quantity": 1, "price_at_purchase": book.price}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({"message": "Đã thêm vào giỏ hàng", "book": book.title})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

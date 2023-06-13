from django.http import HttpRequest
from django.shortcuts import redirect, render
from django import views
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import DetailView
from django.http.response import HttpResponseNotFound

from books_api import GoogleBooksAPI

from .models import BookReview
from .forms import BookReviewForm


class BookView(views.View):
    num_of_pages = 4
    books_per_page = 8
    template_name = "books/list.html"

    def get(self, request: HttpRequest):
        search_query = request.GET.get("q", "")
        books = (
            GoogleBooksAPI.fetch_n_books(
                search_query,
                self.books_per_page * self.num_of_pages,
            )
            if search_query
            else []
        )
        if books is None:
            return redirect(reverse("books:list"))

        paginator = Paginator(books, self.books_per_page)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        context = {
            "page_obj": page_obj,
            "search_query": search_query,
        }
        return render(request, self.template_name, context)


class BookDetailView(DetailView):
    model = BookReview
    template_name = "books/detail.html"
    form_class = BookReviewForm

    def get(self, request):
        book_isbn = request.GET.get("isbn", "")
        book = GoogleBooksAPI.fetch_book(book_isbn)
        if book is None:
            return redirect(reverse("books:list") + f"?isbn={book_isbn}")

        reviews = BookReview.objects.filter(book_isbn=book_isbn).order_by("-id")
        review_form = BookReviewForm()

        context = {"book": book, "reviews": reviews, "review_form": review_form}
        return render(request, self.template_name, context)

    def post(self, request):
        book_isbn = request.GET.get("isbn")
        book = GoogleBooksAPI.fetch_book(book_isbn)
        if book is None:
            return redirect(reverse("books:list") + f"?isbn={book_isbn}")

        reviews = BookReview.objects.filter(book_isbn=book_isbn).order_by("-id")
        review_form = BookReviewForm(request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book_isbn=book_isbn,
                user=request.user,
                stars_given=review_form.cleaned_data["stars_given"],
                comment=review_form.cleaned_data["comment"],
            )
            return redirect(reverse("books:detail") + f"?isbn={book_isbn}")

        context = {"book": book, "reviews": reviews, "review_form": review_form}
        return render(request, self.template_name, context)


class EditReviewView(views.View, LoginRequiredMixin):
    def get(self, request: HttpRequest, review_id):
        review = BookReview.objects.get(pk=review_id)
        book = GoogleBooksAPI.fetch_book(review.book_isbn)
        if book is None:
            raise HttpResponseNotFound("No book match found")

        review_form = BookReviewForm()

        context = {"book": book, "review": review, "review_form": review_form}
        return render(request, "books/edit_review.html", context)

    def post(self, request: HttpRequest, review_id):
        review = BookReview.objects.get(pk=review_id)
        book = GoogleBooksAPI.fetch_book(review.book_isbn)
        if book is None:
            raise HttpResponseNotFound("No book match found")

        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            review_form.save(review_id)
            return redirect(reverse("books:detail") + f"?isbn={book.isbn}")

        context = {"book": book, "review": review, "review_form": review_form}
        return render(request, "books/edit_review.html", context)


class ConfirmDeleteReviewView(views.View, LoginRequiredMixin):
    def get(self, request: HttpRequest, review_id):
        review = BookReview.objects.get(pk=review_id)
        book = GoogleBooksAPI.fetch_book(review.book_isbn)
        if book is None:
            raise HttpResponseNotFound("No book match found")

        context = {"book": book, "review": review}
        return render(request, "books/confirm_delete_review.html", context)


class DeleteReviewView(views.View, LoginRequiredMixin):
    def get(self, request: HttpRequest, review_id):
        review = BookReview.objects.get(pk=review_id)
        book = GoogleBooksAPI.fetch_book(review.book_isbn)
        if book is None:
            raise HttpResponseNotFound("No book match found")

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse("books:detail") + f"?isbn={book.isbn}")

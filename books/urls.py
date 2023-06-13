from django.urls import path, re_path

from books.views import (
    BookDetailView,
    BookView,
    ConfirmDeleteReviewView,
    DeleteReviewView,
    EditReviewView,
)

app_name = "books"
urlpatterns = [
    path("", BookView.as_view(), name="list"),
    path("detail/<int:review_id>/edit/", EditReviewView.as_view(), name="edit-review"),
    re_path(r"^detail/?$", BookDetailView.as_view(), name="detail"),
    path(
        "reviews/<int:review_id>/delete/",
        DeleteReviewView.as_view(),
        name="delete-review",
    ),
    path(
        "reviews/<int:review_id>/delete/confirm/",
        ConfirmDeleteReviewView.as_view(),
        name="confirm-delete-review",
    ),
]

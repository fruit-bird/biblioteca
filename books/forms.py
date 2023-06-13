from django import forms

from .models import BookReview


class BookReviewForm(forms.Form):
    stars_given = forms.IntegerField(min_value=1, max_value=5, required=True)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, review_id):
        review = BookReview.objects.get(id=review_id)
        review.stars_given = self.cleaned_data["stars_given"]
        review.comment = self.cleaned_data["comment"]
        review.save()
        return review

    class Meta:
        model = BookReview
        fields = ("stars_given", "comment")

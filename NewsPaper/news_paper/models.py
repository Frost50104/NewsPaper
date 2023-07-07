from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentrating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentrating')

        self.authorRating = pRat * 3 + cRat
        self.save()

    # def update_rating(self):
    #     UpRatingPost = self.post_set.aggregate(postrating=sum('rating'))
    #     prating = 0
    #     prating += UpRatingPost.get('postrating')
    #
    #     UpRatingComment = self.authorUser.comment_set.aggregate(commentrating=sum('(rating)'))
    #     crating = 0
    #     crating += UpRatingComment.get('commentrating')
    #
    #     self.authorRating = prating * 3 + crating
    #     self.save()

class Category(models.Model):
    categoryname = models.CharField(max_length=64, unique=True)

class Post(models.Model):

    article = 'AR'
    news = 'NW'

    CONTENT_TYPES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=CONTENT_TYPES, default=article)
    createDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


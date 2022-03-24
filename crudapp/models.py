import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    created_at = models.DateField(auto_now= True)
    updated_at = models.DateField(auto_now_add= True)
    
    class Meta:
        abstract = True

class Todo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    todo_title = models.CharField(max_length=100)
    todo_description = models.TextField()
    is_done = models.BooleanField(default=False)

class TimingTodo(BaseModel):
    todo = models.ForeignKey(Todo , on_delete=models.CASCADE)
    timing = models.DateField()


class User(models.Model):
    username = models.TextField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="")
    password = models.TextField(max_length=55, default="")
    # newpassword = models.TextField(max_length=55, default="")

    def __str__(self):
        return self.username

class ItemsList(models.Model):
    item = models.TextField(max_length=255, default='')
    price = models.TextField(max_length=255, default='')
    quantity = models.TextField(max_length=200, default='')

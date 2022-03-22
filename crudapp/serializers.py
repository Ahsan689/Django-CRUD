# serializers.py
from dataclasses import field
from rest_framework import serializers

from .models import *
import re
from django.template.defaultfilters import slugify

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    # Meta class main hume batana parta hai, humari PersonSerializer ki class kis model ko point out kr rhi hai.
    class Meta:
        model = Person
        # yahan pe aap wo fields add kroge jisko aapne serialize krna hai.
        fields = ('id','first_name','last_name')

        # excule = ['first_name']
        # jis field ko exclude krna hai, usko pass krdo, iske ilawa sari fields serialize ho jayengi.

class TodoSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        # yahan pe aap wo fields add kroge jisko aapne serialize krna hai.
        fields = ['user','todo_title','todo_description','slug','uid','is_done']

    def get_slug(self, obj):
        return "crud new app"

    def validate(self , validated_data):
        if validated_data.get('todo_title'):
            todo_title = validated_data['todo_title']
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

            # if len(todo_title < 3):
            #     raise  serializers.ValidationError('todo must be more than 3 characters.')
            # Pass the string in search
            # method of regex object.   
            if not regex.search(todo_title) == None:
                raise  serializers.ValidationError('todo contains special characters.')

        return validated_data


class TimingTodoSerializer(serializers.ModelSerializer):
    todo = TodoSerializer()
    class Meta:
        model = TimingTodo
        exclude = ['created_at','updated_at']
        # agar hume forign key k sath koi object chayye to hum depth pass krte hian, lekin depth main masla ye hai k ye saari fields ko serialize kr k return krdeta hai. jo hum ne serializer main inlude bh nh kri. 
        
        # depth = 1
                    
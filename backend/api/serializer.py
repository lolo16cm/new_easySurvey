#Serialization is the process of converting complex data (like model instances) into simpler, standard formats (such as JSON or XML) that can be easily transmitted over the web or saved. Deserializer is the opposite.
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from userauths.models import User, Profile
from creator.models import Survey, Question, Option
from taker.models import Response, Answer
from django.contrib.auth.password_validation import validate_password


# token and user models -> serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attr
    
    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )

        email_username, _ = user.email.split("@")
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
# metadata: information that describes or provides additional context about data or objects, but it is not the actual content itself.
    class Meta:
        model = User
        #fileds will pass, so no sensitive fileds should be passed, eg opt 
        fields = '__all__'

class ProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Profile
        filed = '__all__'




# creator model to serializer
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__' #['id','text'] 


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)  # Nested serializer for options
    class Meta:
        model = Question
        fields = '__all__' #['id', 'text', 'question_type', 'options']


class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Survey
        fields = ['user', 'title', 'description', 'created_at', 'is_published']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        questions_bank = validated_data.pop('questions')
        # unpack the form dictionary data, survey obj is the survey form
        survey = Survey.objects.create(**validated_data)

        
        for question_data in questions_bank:
            # options_dat either list or None
            options_data = question_data.pop('options', [])  
            # unpack question_data
            # form field in question model
            question = Question.objects.create(form=survey, **question_data)

            # Only add options for question types that require them
            if question.question_type in ['multiple_choice', 'checkbox', 'dropdown'] and options_data:
                for option_data in options_data:
                    Option.objects.create(question=question, **option_data)        
        return survey


# response form model to serializer
class AnswerSerializer(serializers.ModelSerializer):
    selected_options = OptionSerializer(many=True, read_only=True)  # Nested serializer for selected options
    question = serializers.StringRelatedField()  

    class Meta:
        model = Response
        fields ='__all__'




# quesstion answers -> serializer
class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # Nested serializer for answers
    user = serializers.StringRelatedField()  # return __str__ -> self.email
    form = serializers.StringRelatedField()  # return __str__

    class Meta:
        model = Response
        fields = '__all__'

from rest_framework import serializers
from .models import User, UserProfile, Hobby
from blog.serializers import ArticleSerializer


class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()

    def get_same_hobby_users(self, obj):
        user = self.context["request"].user
        return [up.user.username for up in obj.userprofile_set.exclude(user=user)]

    class Meta:
        model = Hobby
        fields = ["name", "same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True, read_only=True)
    get_hobbys = serializers.ListField(required=False)

    class Meta:
        model = UserProfile
        fields = ["description", "nickname", "age", "hobby", "get_hobbys"]


EMAIL_LIST = ["naver.com", "gmail.com"]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    article_set = ArticleSerializer(many=True)


    def validate(self, data):
        if data.get("email", "").split('@')[-1] not in EMAIL_LIST:
            raise serializers.ValidationError(
                detail={"error": "올바른 이메일 형식이 아닙니다."}
            )
        return data

    def create(self, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        user_profile = UserProfile.objects.create(user=user, **user_profile)
        user_profile.hobby.add(*get_hobbys)
        user_profile.save()

        return user

    def update(self, instance, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()

        user_profile_object = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_object, key, value)
        user_profile_object.save()
        user_profile_object.hobby.set(get_hobbys)

        return instance

    class Meta:
        model = User
        fields = ["username", "email", "fullname", "userprofile", "article_set", "join_date", "password"]

        extra_kwargs = {
            'password': {'write_only': True},  # default : False
            'email': {
                'error_messages': {
                    'required': '이메일을 입력해주세요.',
                    'invalid': '올바른 이메일 형식을 입력해주세요.'
                },
                'required': False  # default : True
            },
            'username': {
                'error_messages': {
                    'required': '아이디를 입력해주세요.',
                },
                'required': True
            },
            'fullname': {
                'error_messages': {
                    'required': '이름을 입력해주세요.',
                },
                'required': True
            }
        }
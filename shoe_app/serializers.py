from rest_framework import serializers

from shoe_app.models import Category, Shoe, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'
        depth = 1


class CreateShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    shoe_name = serializers.CharField(source='shoe.name', read_only=True)
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'shoe', 'user',  'shoe_name', 'user_full_name', 'rating', 'comment', 'created_at']

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['user', 'created_at']

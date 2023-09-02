from django.core.exceptions import ValidationError
from rest_framework import serializers, exceptions

from .models import Conference, Tag, Grant


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ('un_name', )


class ConferenceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ('id', 'conf_date_begin', 'conf_date_end')


class ConferenceSerializer(serializers.ModelSerializer):
    is_favorite = serializers.BooleanField(read_only=True)
    tags = TagSerializer(many=True, required=False)
    item_id = serializers.CharField(required=False)

    def create(self, validated_data):
        tag_list = None
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            tag_list = self.get_new_tags(tags_data)

        conf = self.Meta.model.objects.create(**validated_data)
        if tag_list:
            conf.tags.set(tag_list)
        return conf

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            tag_list = self.get_new_tags(tags_data)
            instance.tags.set(tag_list, clear=True)
        return super().update(instance, validated_data)

    @staticmethod
    def get_new_tags(tags_data: list) -> list[Tag]:
        tag_list = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tag_list.append(tag)
        return tag_list

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except ValidationError as e:
            raise exceptions.ValidationError(e.error_dict)

    class Meta:
        model = Conference
        fields = ('id', 'item_id', 'un_name', 'local',
                  'reg_date_begin', 'reg_date_end', 'conf_date_begin',
                  'conf_date_end', 'source_href', 'reg_href',
                  'title', 'short_description', 'description', 'org_name',
                  'themes', 'online', 'conf_href', 'offline', 'conf_address',
                  'contacts', 'rinc', 'tags', 'vak', 'wos', 'scopus', 'conf_status', 'is_favorite')


class GrantSerializer(ConferenceSerializer):
    class Meta:
        model = Grant
        fields = ('un_name', 'local', 'reg_date_begin', 'reg_date_end',
                  'source_href', 'reg_href', 'title', 'short_description', 'description',
                  'contacts', 'checked', 'tags', 'item_id',)

from rest_framework.serializers import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in value.get('link_to_video'):
            raise ValidationError('Ссылка должна быть с youtube.com')

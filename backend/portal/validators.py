from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    def __init__(self, max_mb=10):
        self.max_mb = max_mb

    def __call__(self, value):
        limit = self.max_mb * 1024 * 1024
        if value.size > limit:
            raise ValidationError(f"El archivo no puede superar {self.max_mb} MB.")


    def __eq__(self, other):
        return (
            isinstance(other, FileSizeValidator) and
            self.max_mb == other.max_mb
        )
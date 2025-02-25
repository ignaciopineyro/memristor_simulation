import re

from rest_framework import serializers


class CamelCaseSerializer(serializers.Serializer):
    def __init__(
        self,
        *args,
        allow_null_in_deserialization=False,
        allow_null_in_serialization=False,
        **kwargs
    ):
        self.allow_null_in_deserialization = allow_null_in_deserialization
        self.allow_null_in_serialization = allow_null_in_serialization
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        super(CamelCaseSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        super(CamelCaseSerializer, self).create(validated_data)

    def to_representation(self, instance):
        result = super(CamelCaseSerializer, self).to_representation(instance)
        camel_case_result = CaseAdapter.to_camel_case(
            result, allow_none=self.allow_null_in_serialization
        )
        return camel_case_result

    def to_internal_value(self, data):
        snake_case_data = CaseAdapter.to_snake_case(
            data, allow_none=self.allow_null_in_deserialization
        )
        result = super(CamelCaseSerializer, self).to_internal_value(snake_case_data)
        return result

    @property
    def errors(self):
        snake_case_errors = super(CamelCaseSerializer, self).errors
        camel_case_errors = CaseAdapter.to_camel_case(snake_case_errors)
        return camel_case_errors


class CaseAdapter:
    @classmethod
    def to_camel_case(cls, obj, allow_none=True):
        return cls.transform_case(obj, cls.camel_case_adapter, allow_none)

    @classmethod
    def to_snake_case(cls, obj, allow_none=True):
        return cls.transform_case(obj, cls.snake_case_adapter, allow_none)

    @classmethod
    def transform_case(cls, obj, case_transformer, allow_none=True):
        if isinstance(obj, dict):
            transformed_dict = dict()
            for k, v in obj.items():
                if not allow_none and v is None:
                    continue
                if isinstance(v, dict) or isinstance(v, list):
                    response = cls.transform_case(v, case_transformer)
                    transformed_dict[case_transformer(k)] = response
                else:
                    transformed_dict[case_transformer(k)] = v

            return transformed_dict
        elif isinstance(obj, list):
            transformed_list = list()
            for item in obj:
                transformed_list.append(cls.transform_case(item, case_transformer))
            return transformed_list
        else:
            return obj

    @staticmethod
    def camel_case_adapter(snake_case):
        if isinstance(snake_case, int):
            return snake_case
        first, *others = snake_case.split("_")
        if len(others) == 0:
            return first
        result = "".join([first.lower(), *map(str.title, others)])
        return result

    @staticmethod
    def snake_case_adapter(camel_case):
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_case)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

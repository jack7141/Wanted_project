from typing import Optional
from pydantic.main import ModelMetaclass

class AllOptional(ModelMetaclass):
    def __new__(cls, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {}).copy()

        # Merge annotations from all base classes
        for base in bases:
            if hasattr(base, "__annotations__"):
                annotations.update(base.__annotations__)

        # Make all fields optional
        for field, field_type in annotations.items():
            if not field.startswith("__"):
                annotations[field] = Optional[field_type]

        namespaces["__annotations__"] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)
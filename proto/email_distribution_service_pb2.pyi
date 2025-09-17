from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SendStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[SendStatus]
    SUCCESS: _ClassVar[SendStatus]
    FAILURE: _ClassVar[SendStatus]
    SKIPPED_DUPLICATE: _ClassVar[SendStatus]
UNSPECIFIED: SendStatus
SUCCESS: SendStatus
FAILURE: SendStatus
SKIPPED_DUPLICATE: SendStatus

class SendMailRequest(_message.Message):
    __slots__ = ("template_name", "recipients", "variables")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TEMPLATE_NAME_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    template_name: str
    recipients: _containers.RepeatedScalarFieldContainer[str]
    variables: _containers.ScalarMap[str, str]
    def __init__(self, template_name: _Optional[str] = ..., recipients: _Optional[_Iterable[str]] = ..., variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RecipientSendStatus(_message.Message):
    __slots__ = ("email", "status")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    email: str
    status: SendStatus
    def __init__(self, email: _Optional[str] = ..., status: _Optional[_Union[SendStatus, str]] = ...) -> None: ...

class SendMailResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[RecipientSendStatus]
    def __init__(self, results: _Optional[_Iterable[_Union[RecipientSendStatus, _Mapping]]] = ...) -> None: ...

class GetStatsByEmailRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class TemplateCount(_message.Message):
    __slots__ = ("template_name", "count")
    TEMPLATE_NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    template_name: str
    count: int
    def __init__(self, template_name: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetStatsByEmailResponse(_message.Message):
    __slots__ = ("total_sent", "by_template")
    TOTAL_SENT_FIELD_NUMBER: _ClassVar[int]
    BY_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    total_sent: int
    by_template: _containers.RepeatedCompositeFieldContainer[TemplateCount]
    def __init__(self, total_sent: _Optional[int] = ..., by_template: _Optional[_Iterable[_Union[TemplateCount, _Mapping]]] = ...) -> None: ...

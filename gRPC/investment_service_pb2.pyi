from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetInvestmentsByAccountRequest(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    def __init__(self, account_id: _Optional[str] = ...) -> None: ...

class GetInvestmentsByAccountResponse(_message.Message):
    __slots__ = ("account_id", "investments")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTMENTS_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    investments: _containers.RepeatedCompositeFieldContainer[Investment]
    def __init__(self, account_id: _Optional[str] = ..., investments: _Optional[_Iterable[_Union[Investment, _Mapping]]] = ...) -> None: ...

class GetInvestmentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetInvestmentsResponse(_message.Message):
    __slots__ = ("possible_investments",)
    POSSIBLE_INVESTMENTS_FIELD_NUMBER: _ClassVar[int]
    possible_investments: _containers.RepeatedCompositeFieldContainer[Investment]
    def __init__(self, possible_investments: _Optional[_Iterable[_Union[Investment, _Mapping]]] = ...) -> None: ...

class InvestRequest(_message.Message):
    __slots__ = ("account_id", "investment_id", "amount")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTMENT_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    investment_id: str
    amount: float
    def __init__(self, account_id: _Optional[str] = ..., investment_id: _Optional[str] = ..., amount: _Optional[float] = ...) -> None: ...

class InvestResponse(_message.Message):
    __slots__ = ("message", "investment")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INVESTMENT_FIELD_NUMBER: _ClassVar[int]
    message: str
    investment: Investment
    def __init__(self, message: _Optional[str] = ..., investment: _Optional[_Union[Investment, _Mapping]] = ...) -> None: ...

class Investment(_message.Message):
    __slots__ = ("id", "name", "amount")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    amount: float
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., amount: _Optional[float] = ...) -> None: ...

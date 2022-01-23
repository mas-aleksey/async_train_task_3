from typing import ClassVar, Type, List, Optional
from dataclasses import field
from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class File:
    file_name: Optional[str]
    mime_type: Optional[str]
    thumb: Optional[dict]
    file_id: str
    file_unique_id: str
    file_size: int
    file_path: Optional[str]
    duration: Optional[int]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Info:
    id: int
    first_name: str
    last_name: Optional[str]
    username: str

@dataclass
class From(Info):
    is_bot: bool
    language_code: Optional[str]

@dataclass
class Chat(Info):
    type: str

@dataclass
class Message:
    message_id: int
    from_: From = field(metadata={'data_key': 'from'})
    chat: Chat 
    date: int
    text: Optional[str]
    document: Optional[File]
    animation: Optional[File]
    entities: Optional[list]


@dataclass
class UpdateObj:
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetFileResponse:
    ok: bool
    result: File

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

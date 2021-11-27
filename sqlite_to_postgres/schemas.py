import uuid

from datetime import datetime
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FilmWorkWithoutField:
    title: str
    description: str
    creation_date: datetime
    certificate: str
    type: str
    file_path: str
    created_at: datetime
    updated_at: datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreWithoutField:
    name: str
    created_at: datetime
    updated_at: datetime
    description: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreFilmWorkWithoutField:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonWithoutField:
    birth_date: datetime
    full_name: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonFilmWithoutField:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)

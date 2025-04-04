
#modelagem do banco de dados

from datetime import datetime
from  sqlalchemy import func
from sqlalchemy.orm import registry, Mapped, mapped_column

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True) #identificador (numero da linhas)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

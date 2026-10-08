from sqlalchemy import String,Float,Numeric
from sqlalchemy.orm import Mapped,mapped_column
from database.database import Base 

class Product(Base):
    __tablename__ = "product"

    pro_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    pro_name: Mapped[str] = mapped_column(
        String[100],
        nullable=False
    )

    pro_cat: Mapped[str] = mapped_column(
        String[100],
        nullable=False
    )

    pro_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
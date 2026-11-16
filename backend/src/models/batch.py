from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Text
from src.config.database import Base
class ThermalBatch(Base):
 __tablename__='thermal_batches'
 id:Mapped[int]=mapped_column(primary_key=True)
 name:Mapped[str]=mapped_column(String(150),unique=True)
 filename:Mapped[str]=mapped_column(String(180))
 description:Mapped[str]=mapped_column(Text,default='')

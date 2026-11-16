from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey,UniqueConstraint,DateTime,Float
from datetime import datetime
from src.config.database import Base
class TemperaturePoint(Base):
 __tablename__='temperature_points'
 __table_args__=(UniqueConstraint('batch_id','sequence'),UniqueConstraint('batch_id','recorded_at'))
 id:Mapped[int]=mapped_column(primary_key=True)
 batch_id:Mapped[int]=mapped_column(ForeignKey('thermal_batches.id'))
 sequence:Mapped[int]=mapped_column()
 recorded_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
 temperature:Mapped[float]=mapped_column(Float)

import datetime
from sqlalchemy import Column, Integer, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///Pajamos.db')


class Duomenubaze(Base):
    __tablename__ = 'Pajamos_ir_islaidos'
    id = Column(Integer, primary_key=True)
    iraso_data = Column('Įrašo data', DateTime, default=datetime.date.today())
    dienos_pajamos = Column('Dienos pajamos', Float)
    islaidos_kurui = Column('Išlaidos kurui', Float)
    nuvaziuotas_atstumas = Column('Nuvažiuotas atstumas', Float)
    kitos_islaidos = Column('Kitos išlaidos', Float)

    def __init__(self, iraso_data, dienos_pajamos=0.0, islaidos_kurui=0.0,
                 nuvaziuotas_atstumas=0.0, kitos_islaidos=0.0):
        self.iraso_data = iraso_data
        self.dienos_pajamos = dienos_pajamos
        self.islaidos_kurui = islaidos_kurui
        self.nuvaziuotas_atstumas = nuvaziuotas_atstumas
        self.kitos_islaidos = kitos_islaidos

    def __repr__(self):
        return f'{self.iraso_data} {self.dienos_pajamos} {self.islaidos_kurui}' \
               f' {self.nuvaziuotas_atstumas} {self.kitos_islaidos}'


Base.metadata.create_all(engine)

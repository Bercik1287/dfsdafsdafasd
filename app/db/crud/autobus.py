from sqlalchemy.orm import Session
from ..models.system import Autobusy, Kierowcy, Brygady, Przystanki, Warianty, Trasy, Linie
from ..schema.autobus import LiniaInCreate, AutobusInCreate, KierowcaInCreate, BrygadaInCreate, PrzystanekInCreate, WariantInCreate, TrasaInCreate, LiniaInCreate
from sqlalchemy.exc import IntegrityError

#autobus
def create_autobus(db: Session, autobus: AutobusInCreate):
    db_autobus = Autobusy(
        rejestracja=autobus.rejestracja,
        marka=autobus.marka,
        model=autobus.model
    )
    db.add(db_autobus)
    db.commit()
    db.refresh(db_autobus)
    return db_autobus

#kierowca
def create_kierowca(db: Session, kierowca: KierowcaInCreate):
    db_kierowca = Kierowcy(
        imie=kierowca.imie,
        nazwisko=kierowca.nazwisko,
        pesel=kierowca.pesel
    )
    db.add(db_kierowca)
    db.commit()
    db.refresh(db_kierowca)
    return db_kierowca

def create_brygada(db: Session, brygada: BrygadaInCreate):
    db_brygada = Brygady(nazwa=brygada.nazwa)
    db.add(db_brygada)
    db.commit()
    db.refresh(db_brygada)
    return db_brygada

def create_przystanek(db: Session, przystanek: PrzystanekInCreate):
    db_przystanek = Przystanki(
        nazwa=przystanek.nazwa,
        longi=przystanek.longi,
        lati=przystanek.lati,
        ulica=przystanek.ulica
    )
    db.add(db_przystanek)
    db.commit()
    db.refresh(db_przystanek)
    return db_przystanek

def create_wariant(db: Session, wariant: WariantInCreate):
    db_wariant = Warianty(
        nazwa=wariant.nazwa,
        kod_wariantu=wariant.kod_wariantu
    )
    db.add(db_wariant)
    db.commit()
    db.refresh(db_wariant)
    return db_wariant

def create_trasa(db: Session, trasa: TrasaInCreate):
    db_trasa = Trasy(nazwa=trasa.nazwa)
    db.add(db_trasa)
    db.commit()
    db.refresh(db_trasa)
    return db_trasa

def create_linie(db: Session, linia: LiniaInCreate):
    try:
        db_linia = Linie(
            numer=linia.numer,
            kierunek=linia.kierunek,
            opis=linia.opis
        )
        db.add(db_linia)
        db.commit()
        db.refresh(db_linia)
        return db_linia
    except IntegrityError:
        db.rollback()
        raise


#GET

def get_linie(db: Session):
    return db.query(Linie).order_by(Linie.numer.asc()).all()

def get_przystanki(db: Session):
    return db.query(Przystanki).all()
from sqlalchemy.orm import Session
from ..models.system import Autobusy, Kierowcy, Brygady, Przystanki, Warianty, Trasy, Linie, Linie_Trasy
from ..schema.autobus import (
    LiniaInCreate, AutobusInCreate, KierowcaInCreate, BrygadaInCreate, 
    PrzystanekInCreate, WariantInCreate, TrasaInCreate, LiniaInCreate,
    AutobusInUpdate, KierowcaInUpdate, BrygadaInUpdate, PrzystanekInUpdate,
    WariantInUpdate, TrasaInUpdate, LiniaInUpdate
)
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

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

def get_linia_by_id(db: Session, linia_id: int):
    return db.query(Linie).filter(Linie.id == linia_id).first()

def get_przystanki(db: Session):
    return db.query(Przystanki).all()

def get_przystanek_by_id(db: Session, przystanek_id: int):
    return db.query(Przystanki).filter(Przystanki.id == przystanek_id).first()

def get_autobusy(db: Session):
    return db.query(Autobusy).all()

def get_autobus_by_id(db: Session, autobus_id: int):
    return db.query(Autobusy).filter(Autobusy.id == autobus_id).first()

def get_kierowcy(db: Session):
    return db.query(Kierowcy).all()

def get_kierowca_by_id(db: Session, kierowca_id: int):
    return db.query(Kierowcy).filter(Kierowcy.id == kierowca_id).first()

def get_brygady(db: Session):
    return db.query(Brygady).order_by(Brygady.nazwa).all()

def get_brygada_by_id(db: Session, brygada_id: int):
    return db.query(Brygady).filter(Brygady.id == brygada_id).first()

def get_trasy(db: Session):
    return db.query(Trasy).all()

def get_trasa_by_id(db: Session, trasa_id: int):
    return db.query(Trasy).filter(Trasy.id == trasa_id).first()

def get_warianty(db: Session):
    return db.query(Warianty).all()

def get_wariant_by_id(db: Session, wariant_id: int):
    return db.query(Warianty).filter(Warianty.id == wariant_id).first()

#ALTER
def update_autobus(db: Session, autobus_update: AutobusInUpdate):
    db_autobus = db.query(Autobusy).filter(Autobusy.id == autobus_update.id).first()
    if not db_autobus:
        raise HTTPException(status_code=404, detail="Autobus nie został znaleziony")
    
    update_data = autobus_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_autobus, key, value)
    
    try:
        db.commit()
        db.refresh(db_autobus)
        return db_autobus
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Numer rejestracyjny już istnieje w systemie!")

def update_kierowca(db: Session, kierowca_update: KierowcaInUpdate):
    db_kierowca = db.query(Kierowcy).filter(Kierowcy.id == kierowca_update.id).first()
    if not db_kierowca:
        raise HTTPException(status_code=404, detail="Kierowca nie został znaleziony")
    
    update_data = kierowca_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_kierowca, key, value)
    
    try:
        db.commit()
        db.refresh(db_kierowca)
        return db_kierowca
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="PESEL już istnieje w systemie!")

def update_brygada(db: Session, brygada_update: BrygadaInUpdate):
    db_brygada = db.query(Brygady).filter(Brygady.id == brygada_update.id).first()
    if not db_brygada:
        raise HTTPException(status_code=404, detail="Brygada nie została znaleziona")
    
    update_data = brygada_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_brygada, key, value)
    
    try:
        db.commit()
        db.refresh(db_brygada)
        return db_brygada
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Brygada o tej nazwie już istnieje!")

def update_przystanek(db: Session, przystanek_update: PrzystanekInUpdate):
    db_przystanek = db.query(Przystanki).filter(Przystanki.id == przystanek_update.id).first()
    if not db_przystanek:
        raise HTTPException(status_code=404, detail="Przystanek nie został znaleziony")
    
    update_data = przystanek_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_przystanek, key, value)
    
    try:
        db.commit()
        db.refresh(db_przystanek)
        return db_przystanek
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Przystanek o tej nazwie już istnieje!")

def update_linia(db: Session, linia_update: LiniaInUpdate):
    db_linia = db.query(Linie).filter(Linie.id == linia_update.id).first()
    if not db_linia:
        raise HTTPException(status_code=404, detail="Linia nie została znaleziona")
    
    update_data = linia_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_linia, key, value)
    
    try:
        db.commit()
        db.refresh(db_linia)
        return db_linia
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Linia o tym numerze już istnieje!")

def update_trasa(db: Session, trasa_update: TrasaInUpdate):
    db_trasa = db.query(Trasy).filter(Trasy.id == trasa_update.id).first()
    if not db_trasa:
        raise HTTPException(status_code=404, detail="Trasa nie została znaleziona")
    
    update_data = trasa_update.dict(exclude_unset=True, exclude={'id'})
    for key, value in update_data.items():
        if value is not None:
            setattr(db_trasa, key, value)
    
    try:
        db.commit()
        db.refresh(db_trasa)
        return db_trasa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Trasa o tej nazwie już istnieje!")

def update_wariant(db: Session, wariant_update: WariantInUpdate):
    db_wariant = db.query(Warianty).filter(Warianty.id == wariant_update.id).first()
    if not db_wariant:
        raise HTTPException(status_code=404, detail="Wariant nie został znaleziony")
    
    update_data = wariant_update.dict(exclude_unset=True, exclude={'id'})
    # Handle the 'kod' field mapping to 'kod_wariantu' in the model
    if 'kod' in update_data:
        update_data['kod_wariantu'] = update_data.pop('kod')
    
    for key, value in update_data.items():
        if value is not None:
            setattr(db_wariant, key, value)
    
    try:
        db.commit()
        db.refresh(db_wariant)
        return db_wariant
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Kod wariantu już istnieje w systemie!")


#DELETE
def delete_autobus(db: Session, autobus_id: int):
    db_autobus = db.query(Autobusy).filter(Autobusy.id == autobus_id).first()
    if not db_autobus:
        raise HTTPException(status_code=404, detail="Autobus nie został znaleziony")
    
    try:
        db.delete(db_autobus)
        db.commit()
        return {"message": f"Autobus {db_autobus.rejestracja} został usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunąć autobusu - jest używany w systemie")

def delete_kierowca(db: Session, kierowca_id: int):
    db_kierowca = db.query(Kierowcy).filter(Kierowcy.id == kierowca_id).first()
    if not db_kierowca:
        raise HTTPException(status_code=404, detail="Kierowca nie został znaleziony")
    
    try:
        db.delete(db_kierowca)
        db.commit()
        return {"message": f"Kierowca {db_kierowca.imie} {db_kierowca.nazwisko} został usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunąć kierowcy - jest przypisany do brygady")

def delete_brygada(db: Session, brygada_id: int):
    db_brygada = db.query(Brygady).filter(Brygady.id == brygada_id).first()
    if not db_brygada:
        raise HTTPException(status_code=404, detail="Brygada nie została znaleziona")
    
    try:
        db.delete(db_brygada)
        db.commit()
        return {"message": f"Brygada {db_brygada.nazwa} została usunięta"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunąć brygady - ma przypisanych kierowców lub autobusy")

def delete_przystanek(db: Session, przystanek_id: int):
    db_przystanek = db.query(Przystanki).filter(Przystanki.id == przystanek_id).first()
    if not db_przystanek:
        raise HTTPException(status_code=404, detail="Przystanek nie został znaleziony")
    
    try:
        db.delete(db_przystanek)
        db.commit()
        return {"message": f"Przystanek {db_przystanek.nazwa} został usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunąć przystanku - jest używany w trasach")

def delete_linia(db: Session, linia_id: int):
    db_linia = db.query(Linie).filter(Linie.id == linia_id).first()
    if not db_linia:
        raise HTTPException(status_code=404, detail="Linia nie została znaleziona")
    
    try:
        db.delete(db_linia)
        db.commit()
        return {"message": f"Linia {db_linia.numer} została usunięta"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunąć linii - ma przypisane trasy lub brygady")

def delete_trasa(db: Session, trasa_id: int):
    db_trasa = db.query(Trasy).filter(Trasy.id == trasa_id).first()
    if not db_trasa:
        raise HTTPException(status_code=404, detail="Trasa nie została znaleziona")
    
    try:
        db.delete(db_trasa)
        db.commit()
        return {"message": f"Trasa {db_trasa.nazwa} została usunięta"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunąć trasy - jest używana przez linie")

def delete_wariant(db: Session, wariant_id: int):
    db_wariant = db.query(Warianty).filter(Warianty.id == wariant_id).first()
    if not db_wariant:
        raise HTTPException(status_code=404, detail="Wariant nie został znaleziony")
    
    try:
        db.delete(db_wariant)
        db.commit()
        return {"message": f"Wariant {db_wariant.nazwa} został usunięty"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nie można usunąć wariantu - jest używany w trasach")


#generator
def assign_route_to_line(db: Session, line_id: int, route_id: int, line_number: str = None):
    """
    Assign a route to a line
    """
    try:
        # Check if line exists
        line = db.query(Linie).filter(Linie.id == line_id).first()
        if not line:
            raise ValueError(f"Line with ID {line_id} does not exist")
        
        # Check if route exists
        route = db.query(Trasy).filter(Trasy.id == route_id).first()
        if not route:
            raise ValueError(f"Route with ID {route_id} does not exist")
        
        # Check if relationship already exists
        existing = db.query(Linie_Trasy).filter(
            Linie_Trasy.id_linie == line_id,
            Linie_Trasy.id_trasy == route_id
        ).first()
        
        if existing:
            raise ValueError("Route is already assigned to this line")
        
        # Create the relationship
        line_route = Linie_Trasy(
            id_linie=line_id,
            id_trasy=route_id,
            numer_linii=line_number or line.numer
        )
        
        db.add(line_route)
        db.commit()
        db.refresh(line_route)
        
        return line_route
        
    except IntegrityError:
        db.rollback()
        raise ValueError("Database integrity error - check if the relationship already exists")

def remove_route_from_line(db: Session, line_id: int, route_id: int):
    """
    Remove a route from a line
    """
    line_route = db.query(Linie_Trasy).filter(
        Linie_Trasy.id_linie == line_id,
        Linie_Trasy.id_trasy == route_id
    ).first()
    
    if not line_route:
        raise ValueError("Route is not assigned to this line")
    
    db.delete(line_route)
    db.commit()
    
    return {"message": "Route removed from line successfully"}

def get_routes_for_line(db: Session, line_id: int):
    """
    Get all routes assigned to a specific line
    """
    line_routes = db.query(Linie_Trasy, Trasy).join(
        Trasy, Linie_Trasy.id_trasy == Trasy.id
    ).filter(Linie_Trasy.id_linie == line_id).all()
    
    routes = []
    for line_route, route in line_routes:
        routes.append({
            "route_id": route.id,
            "route_name": route.nazwa,
            "line_number": line_route.numer_linii,
            "assignment_id": line_route.id
        })
    
    return routes

def get_lines_for_route(db: Session, route_id: int):
    """
    Get all lines that use a specific route
    """
    route_lines = db.query(Linie_Trasy, Linie).join(
        Linie, Linie_Trasy.id_linie == Linie.id
    ).filter(Linie_Trasy.id_trasy == route_id).all()
    
    lines = []
    for route_line, line in route_lines:
        lines.append({
            "line_id": line.id,
            "line_number": line.numer,
            "line_direction": line.kierunek,
            "line_description": line.opis,
            "assignment_id": route_line.id
        })
    
    return lines
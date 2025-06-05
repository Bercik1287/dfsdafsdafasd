from sqlalchemy.orm import Session
from ..models.system import Autobusy, Kierowcy, Brygady, Przystanki, Warianty, Trasy, Linie, Linie_Trasy
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
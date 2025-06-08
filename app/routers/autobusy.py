from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.db.models.system import Linie_Trasy, Trasy, Kierowcy, Linie, Przystanki, Brygady, Autobusy, Warianty, Przystanki_Warianty, Odjazdy, Warianty_Trasy
from app.db.schema.autobus import (
    TrasaCreate, TrasaResponse, AutobusInCreate, AutobusOutput, LiniaInCreate, LiniaOutput, 
    WariantInCreate, WariantOutput, TrasaInCreate, TrasaOutput, KierowcaInCreate, KierowcaOutput, 
    PrzystanekOutput, PrzystanekInCreate, BrygadaInCreate, BrygadaOutput,
    AutobusInUpdate, KierowcaInUpdate, BrygadaInUpdate, PrzystanekInUpdate,
    WariantInUpdate, TrasaInUpdate, LiniaInUpdate
)
from app.db.crud.autobus import (
    create_linie, create_wariant, create_trasa, create_autobus, create_kierowca, create_brygada, create_przystanek,
    get_autobusy, get_autobus_by_id, get_kierowcy, get_kierowca_by_id, get_brygady, get_brygada_by_id,
    get_trasy, get_trasa_by_id, get_warianty, get_wariant_by_id, get_linia_by_id, get_przystanek_by_id,
    update_autobus, update_kierowca, update_brygada, update_przystanek, update_linia, update_trasa, update_wariant,
    delete_autobus, delete_kierowca, delete_brygada, delete_przystanek, delete_linia, delete_trasa, delete_wariant
)
from app.core.database import get_db
import time
import json
from typing import List

from app.db.schema.autobus import (
    LinieTrasy, LinieTrasy_Response, RouteForLine, 
    LineForRoute, LineWithRoutes, RouteWithLines
)
from app.db.crud.autobus import (
    assign_route_to_line, remove_route_from_line, 
    get_routes_for_line, get_lines_for_route
)

router = APIRouter(
    prefix="/transport",
    tags=["Transport"]
)

# Sekcja autobusów
@router.post(
    "/autobusy",
    response_model=AutobusOutput,
    status_code=201,
    #tags=["Autobusy"]
)
def dodaj_autobus(autobus_data: AutobusInCreate, db: Session = Depends(get_db)):
    try:
        return create_autobus(db, autobus_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Numer rejestracyjny już istnieje w systemie!"
        )
    
@router.post(
    "/kierowcy",
    response_model=KierowcaOutput,
    status_code=201,
    #tags=["Kierowcy"]
)
def dodaj_kierowce(kierowca_data: KierowcaInCreate, db: Session = Depends(get_db)):
    try:
        return create_kierowca(db, kierowca_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="PESEL już istnieje w systemie!"
        )


@router.post(
    "/brygady",
    response_model=BrygadaOutput,
    status_code=201,
    #tags=["Brygady"]
)
def dodaj_brygade(brygada_data: BrygadaInCreate, db: Session = Depends(get_db)):
    try:
        return create_brygada(db, brygada_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Brygada o tej nazwie już istnieje!"
        )
    
@router.post(
    "/przystanki",
    response_model=PrzystanekOutput,
    status_code=201,
    #tags=["Przystanki"]
)
def dodaj_przystanek(przystanek_data: PrzystanekInCreate, db: Session = Depends(get_db)):
    try:
        return create_przystanek(db, przystanek_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Przystanek o tej nazwie już istnieje!"
        )
    
def dodaj_wariant(wariant_data: WariantInCreate, db: Session = Depends(get_db)):
    try:
        return create_wariant(db, wariant_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Kod wariantu już istnieje w systemie!"
        )

@router.post(
    "/trasy",
    response_model=TrasaOutput,
    status_code=201,
    #tags=["Trasy"]
)
def dodaj_trase(trasa_data: TrasaInCreate, db: Session = Depends(get_db)):
    try:
        return create_trasa(db, trasa_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Trasa o tej nazwie już istnieje!"
        )
    
@router.post(
    "/linie",
    response_model=LiniaOutput,
    status_code=201,
    #tags=["Linie"],
    summary="Dodaj nową linię komunikacyjną",
    responses={
        201: {"description": "Linia została pomyślnie dodana"},
        400: {"description": "Błąd walidacji lub duplikat numeru linii"}
    }
)
def dodaj_linie(linia: LiniaInCreate, db: Session = Depends(get_db)):
    print(linia)
    try:
        return create_linie(db, linia)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Linia o numerze {linia.numer} już istnieje w systemie!"
        )

    #get
@router.get("/autobusy", response_model=List[AutobusOutput])
def pobierz_autobusy(db: Session = Depends(get_db)):
    return get_autobusy(db)

@router.get("/autobusy/{autobus_id}", response_model=AutobusOutput)
def pobierz_autobus(autobus_id: int, db: Session = Depends(get_db)):
    autobus = get_autobus_by_id(db, autobus_id)
    if not autobus:
        raise HTTPException(status_code=404, detail="Autobus nie został znaleziony")
    return autobus

@router.get("/kierowcy", response_model=List[KierowcaOutput])
def pobierz_kierowcow(db: Session = Depends(get_db)):
    return get_kierowcy(db)

@router.get("/kierowcy/{kierowca_id}", response_model=KierowcaOutput)
def pobierz_kierowce(kierowca_id: int, db: Session = Depends(get_db)):
    kierowca = get_kierowca_by_id(db, kierowca_id)
    if not kierowca:
        raise HTTPException(status_code=404, detail="Kierowca nie został znaleziony")
    return kierowca

@router.get("/brygady", response_model=List[BrygadaOutput])
def pobierz_brygady(db: Session = Depends(get_db)):
    return get_brygady(db)

@router.get("/brygady/{brygada_id}", response_model=BrygadaOutput)
def pobierz_brygade(brygada_id: int, db: Session = Depends(get_db)):
    brygada = get_brygada_by_id(db, brygada_id)
    if not brygada:
        raise HTTPException(status_code=404, detail="Brygada nie została znaleziona")
    return brygada

@router.get("/linie")
def pobierz_linie(db: Session = Depends(get_db)):
    return db.query(Linie).all()

@router.get("/linie/{linia_id}", response_model=LiniaOutput)
def pobierz_linie_by_id(linia_id: int, db: Session = Depends(get_db)):
    linia = get_linia_by_id(db, linia_id)
    if not linia:
        raise HTTPException(status_code=404, detail="Linia nie została znaleziona")
    return linia

@router.get("/przystanki")
def pobierz_przystanki(db: Session = Depends(get_db)):
    try:
        return db.query(Przystanki).all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd serwera: {str(e)}"
        )

@router.get("/przystanki/{przystanek_id}", response_model=PrzystanekOutput)
def pobierz_przystanek(przystanek_id: int, db: Session = Depends(get_db)):
    przystanek = get_przystanek_by_id(db, przystanek_id)
    if not przystanek:
        raise HTTPException(status_code=404, detail="Przystanek nie został znaleziony")
    return przystanek

@router.get("/trasy")
def pobierz_trasy(db: Session = Depends(get_db)):
    try:
        return db.query(Trasy).all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd serwera: {str(e)}"
        )
    
@router.get("/trasy/{trasa_id}", response_model=TrasaOutput)
def pobierz_trase(trasa_id: int, db: Session = Depends(get_db)):
    trasa = get_trasa_by_id(db, trasa_id)
    if not trasa:
        raise HTTPException(status_code=404, detail="Trasa nie została znaleziona")
    return trasa

@router.get("/warianty")
def pobierz_warianty(db: Session = Depends(get_db)):
    try:
        return db.query(Warianty).all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd serwera: {str(e)}"
        )
    
# nnie działa
@router.get("/warianty/{wariant_id}", response_model=WariantOutput)
def pobierz_wariant(wariant_id: int, db: Session = Depends(get_db)):
    wariant = get_wariant_by_id(db, wariant_id)
    if not wariant:
        raise HTTPException(status_code=404, detail="Wariant nie został znaleziony")
    return wariant

# @router.post(
#     "/rozklad",
#     response_model=RozkladOutput,
#     status_code=201,
#     #tags=["Rozkład"],
#     summary="Dodaj nowy rozkład jazdy",
#     responses={
#         201: {"description": "Rozkład został pomyślnie dodany"},
#         400: {"description": "Błąd walidacji rozkładu"}
#     }
# )
# def dodaj_rozklad(Rozklad: RozkladInCreate, db: Session = Depends(get_db)):
#     try:
#         return create_rozklad(db, rozklad)
#     except IntegrityError:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Linia o numerze {linia.numer} już istnieje w systemie!"
#         )

@router.post("/trasyv2", response_model=TrasaResponse)
def stworz_trase(
    dane: TrasaCreate,
    db: Session = Depends(get_db)
):
    # Walidacja przystanków
    przystanki = []
    for przystanek_id in dane.przystanki_ids:
        przystanek = db.query(Przystanki).get(przystanek_id)
        if not przystanek:
            raise HTTPException(
                status_code=404,
                detail=f"Przystanek o ID {przystanek_id} nie istnieje"
            )
        przystanki.append(przystanek)
    
    if len(przystanki) < 2:
        raise HTTPException(
            status_code=400,
            detail="Trasa musi mieć co najmniej 2 przystanki"
        )

    # Tworzenie trasy
    trasa = Trasy(nazwa=dane.nazwa_trasy)
    db.add(trasa)
    db.flush()

    # Tworzenie wariantu
    wariant = Warianty(
        nazwa=f"{dane.kod_wariantu}",
        kod_wariantu=dane.kod_wariantu,
        godziny_odjazdu=json.dumps(dane.godziny_odjazdu)  # Zapis jako JSON
    )
    db.add(wariant)
    db.flush()

    # Łączenie wariantu z trasą
    wariant_trasa = Warianty_Trasy(
        id_warianty=wariant.id,
        id_trasy=trasa.id
    )
    db.add(wariant_trasa)

    # Dodawanie przystanków do wariantu
    for kolejnosc, przystanek in enumerate(przystanki, start=1):
        pw = Przystanki_Warianty(
            id_przystanki=przystanek.id,
            id_warianty=wariant.id,
            kolejnosc=kolejnosc
        )
        db.add(pw)

    # Dodanie numeru linii jeśli podany
    if dane.numer_linii:
        linia = Linie_Trasy(
            id_trasy=trasa.id,
            numer_linii=dane.numer_linii
        )
        db.add(linia)

    db.commit()
    db.refresh(trasa)
    
    # Przygotowanie odpowiedzi
    return {
        "id": trasa.id,
        "nazwa": trasa.nazwa,
        "wariant": {
            "id": wariant.id,
            "nazwa": wariant.nazwa,
            "kod_wariantu": wariant.kod_wariantu,
            "godziny_odjazdu": json.loads(wariant.godziny_odjazdu)
        },
        "przystanki": przystanki,
        "numer_linii": dane.numer_linii
    }

#trasolinie

@router.post(
    "/linie/{line_id}/trasy/{route_id}",
    response_model=LinieTrasy_Response,
    status_code=201,
    summary="Assign route to line",
    responses={
        201: {"description": "Route successfully assigned to line"},
        400: {"description": "Invalid data or relationship already exists"},
        404: {"description": "Line or route not found"}
    }
)
def assign_route_to_line_endpoint(
    line_id: int, 
    route_id: int, 
    line_number: str = None,
    db: Session = Depends(get_db)
):
    """
    Assign a route to a specific line
    """
    try:
        result = assign_route_to_line(db, line_id, route_id, line_number)
        return LinieTrasy_Response(
            id=result.id,
            line_id=result.id_linie,
            route_id=result.id_trasy,
            line_number=result.numer_linii
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.delete(
    "/linie/{line_id}/trasy/{route_id}",
    status_code=200,
    summary="Remove route from line"
)
def remove_route_from_line_endpoint(
    line_id: int, 
    route_id: int, 
    db: Session = Depends(get_db)
):
    """
    Remove a route assignment from a line
    """
    try:
        result = remove_route_from_line(db, line_id, route_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get(
    "/linie/{line_id}/trasy",
    response_model=List[RouteForLine],
    summary="Get all routes for a line"
)
def get_routes_for_line_endpoint(
    line_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get all routes assigned to a specific line
    """
    try:
        routes = get_routes_for_line(db, line_id)
        return routes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get(
    "/trasy/{route_id}/linie",
    response_model=List[LineForRoute],
    summary="Get all lines using a route"
)
def get_lines_for_route_endpoint(
    route_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get all lines that use a specific route
    """
    try:
        lines = get_lines_for_route(db, route_id)
        return lines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get(
    "/linie/{line_id}/complete",
    response_model=LineWithRoutes,
    summary="Get line with all its routes"
)
def get_line_with_routes(
    line_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get a line with all its assigned routes
    """
    try:
        # Get the line
        line = db.query(Linie).filter(Linie.id == line_id).first()
        if not line:
            raise HTTPException(status_code=404, detail="Line not found")
        
        # Get all routes for this line
        routes = get_routes_for_line(db, line_id)
        
        return LineWithRoutes(
            id=line.id,
            numer=line.numer,
            kierunek=line.kierunek,
            opis=line.opis,
            routes=routes
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get(
    "/trasy/{route_id}/complete",
    response_model=RouteWithLines,
    summary="Get route with all lines using it"
)
def get_route_with_lines(
    route_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get a route with all lines that use it
    """
    try:
        # Get the route
        route = db.query(Trasy).filter(Trasy.id == route_id).first()
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Get all lines for this route
        lines = get_lines_for_route(db, route_id)
        
        return RouteWithLines(
            id=route.id,
            nazwa=route.nazwa,
            lines=lines
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.post(
    "/linie-trasy/batch",
    status_code=201,
    summary="Assign multiple routes to a line at once"
)
def assign_multiple_routes_to_line(
    line_id: int,
    route_ids: List[int],
    db: Session = Depends(get_db)
):
    """
    Assign multiple routes to a line in a single operation
    """
    try:
        results = []
        errors = []
        
        for route_id in route_ids:
            try:
                result = assign_route_to_line(db, line_id, route_id)
                results.append({
                    "route_id": route_id,
                    "status": "success",
                    "assignment_id": result.id
                })
            except ValueError as e:
                errors.append({
                    "route_id": route_id,
                    "status": "error",
                    "message": str(e)
                })
        
        return {
            "success_count": len(results),
            "error_count": len(errors),
            "results": results,
            "errors": errors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
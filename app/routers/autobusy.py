from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.db.models.system import Linie_Trasy, Trasy, Kierowcy, Linie, Przystanki, Brygady, Autobusy, Warianty, Przystanki_Warianty, Odjazdy, Warianty_Trasy
from app.db.schema.autobus import TrasaCreate, TrasaResponse, AutobusInCreate, AutobusOutput, LiniaInCreate, LiniaOutput, WariantInCreate, WariantOutput,  TrasaInCreate, TrasaOutput, AutobusInCreate, AutobusOutput, KierowcaInCreate, KierowcaOutput, PrzystanekOutput, PrzystanekInCreate, BrygadaInCreate, BrygadaOutput
from app.db.crud.autobus import create_linie, create_wariant, create_trasa, create_autobus, create_kierowca, create_brygada, create_przystanek
from app.core.database import get_db
import time
import json

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
@router.get("/linie")
def pobierz_linie(db: Session = Depends(get_db)):

        return db.query(Linie).all()



@router.get("/przystanki")
def pobierz_przystanki(db: Session = Depends(get_db)):
    try:
        return db.query(Przystanki).all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Błąd serwera: {str(e)}"
        )

@router.get(
    "/brygady",
    response_model=list[BrygadaOutput],
    #tags=["Brygady"],
    summary="Pobierz listę brygad"
)
def pobierz_brygady(db: Session = Depends(get_db)):

        return db.query(Brygady).order_by(Brygady.nazwa).all()

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
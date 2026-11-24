from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Calculation, User
from app.schemas import CalculationCreate, CalculationRead
from app.operations.factory import CalculationFactory


router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


@router.get("", response_model=list[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    calculations = db.scalars(
        select(Calculation).order_by(Calculation.id)
    ).all()

    return calculations


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
):
    calculation = db.get(Calculation, calculation_id)

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found",
        )

    return calculation


@router.post("", response_model=CalculationRead, status_code=201)
def add_calculation(
    data: CalculationCreate,
    db: Session = Depends(get_db),
):
    user = db.get(User, data.user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    operation = CalculationFactory.create(data.type)
    result = operation(data.a, data.b)

    calculation = Calculation(
        a=data.a,
        b=data.b,
        type=data.type,
        result=result,
        user_id=data.user_id,
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    return calculation


@router.put("/{calculation_id}", response_model=CalculationRead)
def edit_calculation(
    calculation_id: int,
    data: CalculationCreate,
    db: Session = Depends(get_db),
):
    calculation = db.get(Calculation, calculation_id)

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found",
        )

    user = db.get(User, data.user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    operation = CalculationFactory.create(data.type)
    result = operation(data.a, data.b)

    calculation.a = data.a
    calculation.b = data.b
    calculation.type = data.type
    calculation.result = result
    calculation.user_id = data.user_id

    db.commit()
    db.refresh(calculation)

    return calculation


@router.delete("/{calculation_id}", status_code=204)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
):
    calculation = db.get(Calculation, calculation_id)

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found",
        )

    db.delete(calculation)
    db.commit()

    return None

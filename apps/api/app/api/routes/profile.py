from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ...core.security import current_user

router = APIRouter()

@router.get("")
def get_profile(user=Depends(current_user)):
    return {"id": str(user.id), "email": user.email, "full_name": user.full_name, "role": user.role, "is_active": user.is_active}

@router.put("")
def update_profile(full_name: str | None = None, user=Depends(current_user), db: Session = Depends(get_db)):
    if full_name is not None and full_name.strip():
        user.full_name = full_name.strip()
        db.commit()
        db.refresh(user)
    return {"id": str(user.id), "email": user.email, "full_name": user.full_name, "role": user.role}

@router.put("/preferences")
def update_preferences(preferences: dict, user=Depends(current_user)):
    # Preferences are intentionally returned as a stateless contract until the preference table is migrated.
    return {"user_id": str(user.id), "preferences": preferences}

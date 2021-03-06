from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from dispatch.auth.models import DispatchUser
from dispatch.auth.service import get_current_user
from dispatch.database import get_db, search_filter_sort_paginate
from dispatch.enums import UserRoles

from .models import IncidentTypeCreate, IncidentTypePagination, IncidentTypeRead, IncidentTypeUpdate
from .service import create, get, update


router = APIRouter()


@router.get("/", response_model=IncidentTypePagination, tags=["incident_types"])
def get_incident_types(
    db_session: Session = Depends(get_db),
    page: int = 1,
    items_per_page: int = Query(5, alias="itemsPerPage"),
    query_str: str = Query(None, alias="q"),
    sort_by: List[str] = Query([], alias="sortBy[]"),
    descending: List[bool] = Query([], alias="descending[]"),
    fields: List[str] = Query([], alias="field[]"),
    ops: List[str] = Query([], alias="op[]"),
    values: List[str] = Query([], alias="value[]"),
):
    """
    Returns all incident types.
    """
    return search_filter_sort_paginate(
        db_session=db_session,
        model="IncidentType",
        query_str=query_str,
        page=page,
        items_per_page=items_per_page,
        sort_by=sort_by,
        descending=descending,
        fields=fields,
        values=values,
        ops=ops,
    )


@router.post("/", response_model=IncidentTypeRead)
def create_incident_type(
    *,
    db_session: Session = Depends(get_db),
    incident_type_in: IncidentTypeCreate,
    current_user: DispatchUser = Depends(get_current_user),
):
    """
    Create a new incident type.
    """
    # We restrict the creation of incident types to admins only
    if current_user.role != UserRoles.admin:
        raise HTTPException(
            status_code=403, detail="You do not have permission to create incident types."
        )
    incident_type = create(db_session=db_session, incident_type_in=incident_type_in)
    return incident_type


@router.put("/{incident_type_id}", response_model=IncidentTypeRead)
def update_incident_type(
    *,
    db_session: Session = Depends(get_db),
    incident_type_id: int,
    incident_type_in: IncidentTypeUpdate,
    current_user: DispatchUser = Depends(get_current_user),
):
    """
    Update an existing incident type.
    """
    incident_type = get(db_session=db_session, incident_type_id=incident_type_id)
    if not incident_type:
        raise HTTPException(
            status_code=404, detail="The incident type with this id does not exist."
        )

    # We restrict updating incident types to admins only
    if current_user.role != UserRoles.admin:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update incident types."
        )

    incident_type = update(
        db_session=db_session, incident_type=incident_type, incident_type_in=incident_type_in
    )
    return incident_type


@router.get("/{incident_type_id}", response_model=IncidentTypeRead)
def get_incident_type(*, db_session: Session = Depends(get_db), incident_type_id: int):
    """
    Get an incident type.
    """
    incident_type = get(db_session=db_session, incident_type_id=incident_type_id)
    if not incident_type:
        raise HTTPException(
            status_code=404, detail="The incident type with this id does not exist."
        )
    return incident_type

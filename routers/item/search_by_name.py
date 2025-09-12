#from fastapi import APIRouter, Depends 
#from sqlmodel import select 
#from Models.item import Item 
#from database import get_session 
#from typing import List 
#router = APIRouter() 
#@router.get("/Search_by_name", response_model=List[Item]) 
#def search_items_by_name(name: str, session=Depends(get_session)): 
#    query = select(Item).where(Item.name.contains(name))
#    return session.exec(query).all() 
#if not item: 
# #raise HTTPException(status_code=404, detail="کالا با این SKU پیدا نشد") 
# #return item
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from Models.item import Item
from database import get_session
from typing import List

router = APIRouter()

@router.get("/Search_by_name", response_model=List[Item])
def search_items_by_name(name: str, session=Depends(get_session)):
    query = select(Item).where(Item.name.contains(name))
    items = session.exec(query).all()

    if not items:
        raise HTTPException(status_code=404, detail="هیچ کالایی با این نام پیدا نشد")

    return items

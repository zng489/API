conda activate great_expectations

http://localhost:8000/docs

$ pip install fastapi

$ pip install uvicorn

https://medium.com/@vinicius_/como-criar-uma-api-rest-usando-python-com-fastapi-framework-1701849c0ce6

https://www.youtube.com/watch?v=tpT48Rpt-Ww

https://www.youtube.com/watch?v=XnYYwcOfcn8

https://www.youtube.com/watch?v=wS9LfFtXdBs

uvicorn main:app --reload

uvicorn folder.main:app --reload
    item_dict = jsonable_encoder(db_item)
    db.add(item_dict)
    db.commit()
    db.refresh(item_dict)
    return item_dict
 
from typing import Union,Annotated,List

from fastapi import FastAPI,File, UploadFile, HTTPException,Depends,Query,Form,APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from PIL import Image
import io
from pathlib import Path

from torchimg.tools.single_test import *

from sqlmodel import Session, SQLModel, create_engine, select

from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from torchimg.userdb import crud, schemas
# from torchimg.userdb.database import get_db
from torchimg.userdb import models
from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.dao.user_dao import UserDao
from module_admin.service.user_service import UserService
from module_admin.entity.vo.user_vo import (
    AddUserModel,
    CrudUserRoleModel,
    CurrentUserModel,
    DeleteUserModel,
    EditUserModel,
    ResetUserModel,
    SelectedRoleModel,
    UserDetailModel,
    UserInfoModel,
    UserModel,
    UserPageQueryModel,
    UserPostModel,
    UserProfileModel,
    UserRoleModel,
    UserRoleQueryModel,
    UserRoleResponseModel,
)
from utils.pwd_util import PwdUtil
from module_history.entity.do.history_do import History
from module_history.entity.vo.history_vo import HistoryPageModel, HistoryModel
from module_history.service.history_service import HistoryService
from module_admin.service.common_service import CommonService
from module_admin.entity.vo.common_vo import CrudResponseModel, UploadResponseModel
from utils.upload_util import UploadUtil
from exceptions.exception import ServiceException
from datetime import datetime
from config.env import UploadConfig, OSSConfig
from module_history.dao.history_dao import HistoryDao
########       Img Torch

CACHE_DIR = Path("./img_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)



# @asynccontextmanager
# async def lifespan(app: FastAPI):
    # server_load_model()
#     # # Load the ML model
#     # ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
#     yield
#     # # Clean up the ML models and release the resources
#     # ml_models.clear()
#     # server.should_exit = True



########       Img Torch

# app = FastAPI(lifespan=lifespan)

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

torchimg = APIRouter()


def response_success(data=None, msg="操作成功", code=200):
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

def response_error(msg="操作失败", code=500, data=None):
    return {
        "code": code,
        "msg": msg,
        "data": data
    }






@torchimg.post("/myvue/disease-stats", response_model=schemas.BaseResponse[schemas.VueAllClass])
async def get_disease_stats(user: schemas.VueUser, db: AsyncSession = Depends(get_db)):
    type0_records = await HistoryDao.get_vue_count(db=db, type='0', id=int(user.id))
    type1_records = await HistoryDao.get_vue_count(db=db, type='1', id=int(user.id))
    type2_records = await HistoryDao.get_vue_count(db=db, type='2', id=int(user.id))
    type3_records = await HistoryDao.get_vue_count(db=db, type='3', id=int(user.id))
    type4_records = await HistoryDao.get_vue_count(db=db, type='4', id=int(user.id))
    all_records = await HistoryDao.get_vue_count(db=db, type='all', id=int(user.id))
    current_records = await HistoryDao.get_vue_count(db=db, type='current', id=int(user.id))
    return response_success(data=schemas.VueAllClass(
            type0=type0_records,
            type1=type1_records,
            type2=type2_records,
            type3=type3_records,
            type4=type4_records,
            allrecord=all_records,
            currentuserrecord=current_records)
    )
    # return {
    #     "code": 200,
    #     "msg": "查询成功",
    #     "data": schemas.VueAllClass(
    #         type0=type0_records,
    #         type1=type1_records,
    #         type2=type2_records,
    #         type3=type3_records,
    #         type4=type4_records,
    #         allrecord=all_records,
    #         currentuserrecord=current_records
    #     )
    # }
@torchimg.get("/myvue/HistoryData", response_model=schemas.BaseResponse[List[schemas.VueRecords]])
async def load_history_data(db: AsyncSession = Depends(get_db)):
    query = (
        select(History)
        .where(History.del_flag == '0')
        .order_by(desc(History.id))
        .limit(6)
    )
    query_result = await db.execute(query)


    paginated_data = []
    for row in query_result:
        if row and len(row) == 1:
            paginated_data.append(row[0])
        else:
            paginated_data.append(row)

    history_items = [
        schemas.VueRecords(
            id=str(result.id),
            updatedAt=result.time,
            location=result.location,
            user_name=str(result.reportid),
            predclass=result.predclass
        )
        for result in paginated_data
    ]

    return response_success(data=history_items)










########       Database

@torchimg.post("/users/register", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await crud.create_user(db=db, user=user)
    return schemas.User(
                id = result.id,
                name = result.name
            )
    



@torchimg.get("/users/", response_model=schemas.UsersList)
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip, limit)
    return {"users": users}


@torchimg.post("/users/editnamebyid", response_model=schemas.UserCheck)
async def editusernamebyid(user: schemas.User, db: AsyncSession = Depends(get_db)):
    samename = await crud.get_user_by_name(db, name=user.name)
    # print(user.name)
    # print(samename.user_name)
    if user.name == samename.user_name:
            return schemas.UserCheck(
                id=samename.user_id,
                name=samename.user_name,
                checkinfo=False
        )
    if not await crud.edit_username_id(db, user):
        return schemas.UserCheck(
            id=user.id, 
            name=user.name,
            checkinfo=False
        )
    edit_user = await crud.get_user_by_id(db, id=user.id)
    if edit_user and user.name == edit_user.user_name:
        return schemas.UserCheck(
                   id=edit_user.user_id,
                   name=edit_user.user_name,
                   checkinfo=True
        )
    else:
        return schemas.UserCheck(
            id=edit_user.user_id, 
            name=user.name,
            checkinfo=False
        )

@torchimg.post("/users/editpwdbyid", response_model=schemas.UserCheck)
async def editpwdbyid(user: schemas.UserPwd, db: AsyncSession = Depends(get_db)):
    if not await crud.edit_pwd_id(db, user):
        return schemas.UserCheck(
            id=user.id,
            name='NULL',
            checkinfo=False
        )
    edit_user = await crud.get_user_by_id(db, id=user.id)
    if edit_user and PwdUtil.verify_password(user.password, edit_user.password):
        return schemas.UserCheck(
                   id=edit_user.user_id,
                   name=edit_user.user_name,
                   checkinfo=True
        )
    else:
        return schemas.UserCheck(
            id=edit_user.user_id,
            name=edit_user.user_name,
            checkinfo=False
        )

@torchimg.post("/users/logininfo", response_model=schemas.UserInfo)
async def login_users(user: schemas.UserBase, db: AsyncSession = Depends(get_db)):
    temp = UserModel()
    temp.user_id = user.id
    result = await UserDao.get_user_by_info(db=db, user=temp)
    if not result or user.id != 0:
        return schemas.UserInfo(
            user_id=-1,
            dept_id=-1,
            name='NULL',
            nick_name='NULL',
            email='NULL',
            phonenumber='NULL',
            sex = 'NULL'
        )
    else:
        return schemas.UserInfo(
            user_id=result.user_id,
            dept_id=result.dept_id,
            name=result.user_name,
            nick_name=result.nick_name,
            email=result.email,
            phonenumber=result.phonenumber,
            sex = '男' if result.sex == '0' else '女' if result.sex == '1' else '未知'
        )

@torchimg.post("/users/login", response_model=schemas.UserCheck)
async def login_users(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):

    temp = UserModel()
    temp.user_name = user.name
    login_user = await UserDao.get_user_by_info(db=db, user=temp)
    # print("传入Name"+user.name)
    # print("传入Password"+user.password)
    # print("读取Name"+login_user.nick_name)
    # print("读取Password"+login_user.password)
    print(PwdUtil.verify_password(user.password, login_user.password))
    if login_user and PwdUtil.verify_password(user.password, login_user.password):
        return schemas.UserCheck(
            id=login_user.user_id,
            name=login_user.user_name,
            checkinfo=True
        )
    else:
        return schemas.UserCheck(
            id=-1,  # 表示无效用户
            name=user.name,
            checkinfo=False
        )

@torchimg.post("/predict")
async def predict(
    time: str = Form(...),
    location: str = Form(...),
    lat: str = Form(...),
    lng: str = Form(...),
    reportid: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # 检查用户是否存在（异步查询）
    # stmt = select(models.User).where(models.User.id == reportid)
    # result = await db.execute(stmt)
    # user = result.scalars().first()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    
    # 检查reportid是否在User表中存在
    temp = UserModel()
    temp.user_id = reportid
    userresult = await UserDao.get_user_by_info(db=db, user=temp)
    if not userresult:
        raise HTTPException(status_code=404, detail="User with the given reportid not found")
    

    if not UploadUtil.check_file_extension(file):
        raise ServiceException(message='文件类型不合法')
    else:
        relative_path = f'upload/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
        dir_path = os.path.join(UploadConfig.UPLOAD_Record_img_PATH, relative_path)
        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass
        filename = f'{file.filename.rsplit(".", 1)[0]}_{datetime.now().strftime("%Y%m%d%H%M%S")}{UploadConfig.UPLOAD_MACHINE}{UploadUtil.generate_random_number()}.{file.filename.rsplit(".")[-1]}'
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'wb') as f:
                # 流式写出大型文件，这里的10代表10MB
            for chunk in iter(lambda: file.file.read(1024 * 1024 * 10), b''):
                    f.write(chunk)

    print(filepath)
    print(filename)

    # # 处理文件
    # contents = await file.read()
    # filename = CACHE_DIR / f"uploaded_{file.filename}"

    # with open(filename, "wb") as f:
    #     f.write(contents)

    result = server_image(str(filepath))

    history = HistoryModel(
        image=f'{UploadConfig.UPLOAD_Record_img_PREFIX}/{relative_path}/{filename}',
        time=time,
        location=location,
        lat=lat,
        lng=lng,
        reportid=reportid,
        predlabel=str(result['pred_label']),
        predclass=str(result['pred_class']),
        predscore=result['pred_score'],
        del_flag = '0',
        create_by = userresult.user_name,
        dept_id = userresult.dept_id
    )
    await HistoryService.add_history(query_db=db, query_object=history)
    # os.remove(str(filename))
    return JSONResponse(content={
        "pred_class": result['pred_class'],
        "pred_label": result['pred_label'],
        "pred_score": result['pred_score']
    })




# 批量转换函数
async def batch_convert_to_history_item_response(db_session: AsyncSession, records) -> List[schemas.HistoryItemResponse]:
    return [schemas.HistoryItemResponse.from_sqlalchemy_model(record) for record in records]


@torchimg.get("/records/", response_model=schemas.PaginatedResponse)
# @torchimg.get("/records/")
async def get_records(
    page: int = Query(1, ge=1),
    # page: int = Form(...),
    page_size: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    



    # 计算总数和总页数
    total_records = await HistoryDao.get_active_count(db=db)
    total_pages = ceil(total_records / page_size) if total_records else 0
    if total_records > 0:
        if page <= total_pages:
            if page == total_pages:
               current_record = total_records - (page - 1) * page_size
            else:
               current_record = page_size
        else:
            current_record = page_size
    else:
        current_record =  0



    print(  "current_record："+str(current_record) + '\n' +
            "page_size："+str(page_size) + '\n' +
            "total_records："+str(total_records) + '\n' +
            "total_pages："+str(total_pages) + '\n' +
            "has_next_page："+str(page < total_pages) + '\n')

    # # 计算总数和总页数
    # total_records = db.query(func.count(models.History.imageid)).scalar()
    # total_pages = ceil(total_records / page_size) if total_records else 0
    # if total_records > 0:
    #     if page <= total_pages:
    #         if page == total_pages:
    #            current_record = total_records - (page - 1) * page_size
    #         else:
    #            current_record = page_size
    #     else:
    #         current_record = page_size
    # else:
    #     current_record =  0



    
    query = (
        select(History)
        .where(
            History.del_flag == '0'
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(desc(History.id))
    )
    query_result = await db.execute(query)
    # print(query_result)
    # if(query_result):
    paginated_data = []
    for row in query_result:
        if row and len(row) == 1:
            paginated_data.append(row[0])
        else:
            paginated_data.append(row)

    # print(paginated_data)

    history_items: List[schemas.HistoryItemResponse] = []
    for result in paginated_data:
        # 从查询结果中获取字段数据，直接映射到 HistoryItemResponse 模型
        history_item = schemas.HistoryItemResponse(
            imageid=result.id,
            image_base64=result.image,  # 假设 'image' 字段是 Base64 编码的字符串
            time=result.time,
            location=result.location,
            lat=str(result.lat),  # lat 和 lng 可能是浮动的，根据需要转为字符串
            lng=str(result.lng),
            reportid=result.reportid,
            predlabel=result.predlabel,
            predclass=result.predclass,
            predscore=result.predscore,
        )
    
        # 将生成的 HistoryItemResponse 添加到列表中
        history_items.append(history_item)

    print(history_items)
    

    # 构建响应
    return {
        "data": await batch_convert_to_history_item_response(db, history_items),
        "pagination": {
            "current_page": page,
            "current_record": current_record,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages,
            "has_next_page": page < total_pages
        }
    }


@torchimg.get("/image/{imageid}")
async def get_image(imageid: str, db: AsyncSession = Depends(get_db)):
    record = db.query(schemas.HistoryItemResponse).filter(schemas.HistoryItemResponse.imageid == imageid).first()
    return StreamingResponse(
        io.BytesIO(record.image), 
        media_type="image/jpeg",
        headers={"Content-Length": str(len(record.image))}
    )


@torchimg.delete("/cleartable/{tablename}")
def clear_all_data_endpoint(tablename: str,db: AsyncSession = Depends(get_db)):
    return crud.clear_all_data(db,tablename)
########       Database


@torchimg.get("/Hello")
def read_root():
    return {"Hello": "World"}


@torchimg.get("/ping")
async def connectivity_test():
    return JSONResponse(content={"status": "success", "message": "Server is reachable"})

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="File must be an image")

#     # contents = await file.read()
#     # with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
#     #     tmp.write(contents)
#     #     tmp_path = tmp.name

#     contents = await file.read()
#     filename = CACHE_DIR / f"uploaded_{file.filename}"
#     with open(filename, "wb") as f:
#         f.write(contents)

#     result = server_image(str(filename))
#     # os.remove(str(filename))  # Cleanup temp file
#     return JSONResponse(content={"pred_class": result['pred_class'], "pred_label": result['pred_label'],"pred_score":result['pred_score']})


# @torchimg.post("/predict")
# async def predict(
#                   time: str= Form(...),
#                   location: str= Form(...),
#                   lat: str= Form(...),
#                   lng: str= Form(...),
#                   reportid: str= Form(...),
#                   file: UploadFile = File(...),
#                   db: AsyncSession = Depends(get_db)
#                   ):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="File must be an image")

#     # contents = await file.read()
#     # with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
#     #     tmp.write(contents)
#     #     tmp_path = tmp.name


#     # 检查reportid是否在User表中存在
#     user = db.query(models.User).filter(models.User.id == reportid).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User with the given reportid not found")

#     contents = await file.read()
#     filename = CACHE_DIR / f"uploaded_{file.filename}"
#     with open(filename, "wb") as f:
#         f.write(contents)

#     result = server_image(str(filename))
#     os.remove(str(filename))  # Cleanup temp file
    
#     # 创建History实例并填充字段
#     new_history_item = models.History(
#         image=contents,  # 将文件内容作为BLOB存储
#         time=time,
#         location=location,
#         lat=lat,
#         lng=lng,
#         reportid=reportid,  # 假设reportid传入的是字符串类型，会被转换为整数
#         predlabel=result['pred_label'],
#         predclass=result['pred_class'],
#         predscore=result['pred_score']
#     )
#     crud.create_historyitem(db=db,history=new_history_item)
#     # os.remove(str(filename))  # Cleanup temp file
#     return JSONResponse(content={"pred_class": result['pred_class'], "pred_label": result['pred_label'],"pred_score":result['pred_score']})

# @torchimg.post("/predict")
# async def predict(
#     time: str = Form(...),
#     location: str = Form(...),
#     lat: str = Form(...),
#     lng: str = Form(...),
#     reportid: str = Form(...),
#     file: UploadFile = File(...),
#     db: AsyncSession = Depends(get_db)
# ):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="File must be an image")

#     # 检查用户是否存在（异步查询）
#     # stmt = select(models.User).where(models.User.id == reportid)
#     # result = await db.execute(stmt)
#     # user = result.scalars().first()
#     # if not user:
#     #     raise HTTPException(status_code=404, detail="User not found")

#     # 处理文件
#     contents = await file.read()
#     filename = CACHE_DIR / f"uploaded_{file.filename}"
#     with open(filename, "wb") as f:
#         f.write(contents)

#     result = server_image(str(filename))
#     os.remove(str(filename))

#     # # 创建历史记录（异步提交）
#     # new_history_item = models.History(
#     #     image=contents,
#     #     time=time,
#     #     location=location,
#     #     lat=lat,
#     #     lng=lng,
#     #     reportid=reportid,
#     #     predlabel=result['pred_label'],
#     #     predclass=result['pred_class'],
#     #     predscore=result['pred_score']
#     # )
#     # db.add(new_history_item)
#     # await db.commit()

#     return JSONResponse(content={
#         "pred_class": result['pred_class'],
#         "pred_label": result['pred_label'],
#         "pred_score": result['pred_score']
#     })




# # 批量转换函数
# def batch_convert_to_history_item_response(db_session: AsyncSession, records) -> List[schemas.HistoryItemResponse]:
#     return [schemas.HistoryItemResponse.from_sqlalchemy_model(record) for record in records]


# @torchimg.get("/records/", response_model=schemas.PaginatedResponse)
# async def get_records(
#     page: int = Query(1, ge=1),
#     # page: int = Form(...),
#     page_size: int = Query(10, le=100),
#     db: AsyncSession = Depends(get_db)
# ):

#     # 计算总数和总页数
#     total_records = db.query(func.count(models.History.imageid)).scalar()
#     total_pages = ceil(total_records / page_size) if total_records else 0
#     if total_records > 0:
#         if page <= total_pages:
#             if page == total_pages:
#                current_record = total_records - (page - 1) * page_size
#             else:
#                current_record = page_size
#         else:
#             current_record = page_size
#     else:
#         current_record =  0
    



#     # 获取分页数据
#     records = db.query(models.History)\
#         .order_by(models.History.imageid)\
#         .offset((page - 1) * page_size)\
#         .limit(page_size)\
#         .all()
    
#     # # 将 BLOB 数据转换为 base64 编码字符串
#     # for record in records:
#     #     schemas.HistoryItemResponse.from_obj(record)
#     #     # record['image_base64'] = blob_to_base64(record['image'])
#     #     # del record['image']  # 删除原来的 BLOB 字段

#     # 构建响应
#     return {
#         "data": batch_convert_to_history_item_response(db, records),
#         "pagination": {
#             "current_page": page,
#             "current_record": current_record,
#             "page_size": page_size,
#             "total_records": total_records,
#             "total_pages": total_pages,
#             "has_next_page": page < total_pages
#         }
#     }


# @torchimg.get("/image/{imageid}")
# async def get_image(imageid: str, db: AsyncSession = Depends(get_db)):
#     record = db.query(schemas.HistoryItemResponse).filter(schemas.HistoryItemResponse.imageid == imageid).first()
#     return StreamingResponse(
#         io.BytesIO(record.image), 
#         media_type="image/jpeg",
#         headers={"Content-Length": str(len(record.image))}
#     )


# @torchimg.delete("/cleartable/{tablename}")
# def clear_all_data_endpoint(tablename: str,db: AsyncSession = Depends(get_db)):
    # return crud.clear_all_data(db,tablename)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="192.168.31.177", port=8000)
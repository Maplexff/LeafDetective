from module_admin.entity.do.user_do import SysUser
from sqlalchemy import delete,and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from torchimg.userdb import schemas









import io
import pandas as pd
from datetime import datetime
from fastapi import Request, UploadFile,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.user_dao import UserDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.post_vo import PostPageQueryModel
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
from module_admin.service.config_service import ConfigService
from module_admin.service.dept_service import DeptService
from module_admin.service.post_service import PostService
from module_admin.service.role_service import RoleService
from utils.common_util import CamelCaseUtil, export_list2excel, get_excel_template
from utils.page_util import PageResponseModel
from utils.pwd_util import PwdUtil
from utils.log_util import logger
from module_admin.dao.user_dao import UserDao
from module_admin.service.user_service import UserService


async def get_user_by_name(db: AsyncSession, name: str):
    # return db.query(SysUser).filter(SysUser.user_name == name).first()
    return await UserDao.get_user_by_info(db=db, user=UserModel(nick_name=name))


async def get_user_by_id(db: AsyncSession, id: int):
    query_user_basic_info = (
        (
            await db.execute(
                select(SysUser)
                .where(SysUser.status == '0', SysUser.del_flag == '0', SysUser.user_id == id)
                .distinct()
                )
            )
            .scalars()
            .first()
        )    
    return query_user_basic_info
    
    
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    query_user_basic_info = (
        await db.execute(
            select(SysUser)
            .where(SysUser.status == '0', SysUser.del_flag == '0')
            .distinct()  # distinct 应该在 select 查询时使用
            .offset(skip)  # offset 和 limit 放在查询链中
            .limit(limit)
        )
    )
    sys_users = query_user_basic_info.scalars().all()
    # 将查询的 SysUser 对象转化为 Pydantic User 对象
    users = [schemas.User.from_sqlalchemy_model(user) for user in sys_users]  # 使用 from_sqlalchemy_model 转换
    return users


    
    

async def create_user(db: AsyncSession, user: schemas.UserCreate):

    add_user = AddUserModel()
    
    add_user.user_name = user.name
    add_user.nick_name = user.name
    add_user.del_flag = '0'
    add_user.sex='2'
    add_user.status='0'
    add_user.password = PwdUtil.get_password_hash(user.password)
    add_user.create_by = "system"
    add_user.create_time = datetime.now()
    add_user.update_by = "system"
    add_user.update_time = datetime.now()
    add_user.avatar = "/profile/upload/圆角-1744118422914 (1).png"
    role = 2
    # add_user_result = await UserService.add_user_services(db, add_user)
    print(add_user)
    add_user1 = UserModel(**add_user.model_dump(by_alias=True))
    if not await UserService.check_user_name_unique_services(db, add_user1):
        return schemas.User(
                id = -1,
                name = user.name
        )
    elif add_user.nick_name and not await UserService.check_user_nickname_unique_services(db, add_user):
        return schemas.User(
                id = -1,
                name = user.name
        )
    else:
        try:
            add_result = await UserDao.add_user_dao(db, add_user1)
            user_id = add_result.user_id
            await UserDao.add_user_role_dao(db, UserRoleModel(userId=user_id, roleId=2))
            if add_user.post_ids:
                for post in add_user.post_ids:
                    await UserDao.add_user_post_dao(db, UserPostModel(userId=user_id, postId=post))
            await db.commit()
            db_user = await UserDao.get_user_by_info(db=db, user=UserModel(nick_name=user.name))
            if db_user:
                return schemas.User(
                   id = db_user.user_id,
                   name = user.name
             )
        except Exception as e:
            await db.rollback()
            # raise e
            return schemas.User(
                id = -1,
                name = user.name
           )

    # logger.info(add_user_result.message)
    # db_user = await UserDao.get_user_by_info(db=db, user=UserModel(nick_name=user.name))
    # if db_user:
    #     # raise HTTPException(status_code=400, detail="Name already registered")
    #     return schemas.User(
    #             id = db_user.user_id,
    #             name = user.name
    #     )
    # else:
    #     return schemas.User(
    #             id = -1,
    #             name = user.name
    #     )




async def edit_user_services(query_db: AsyncSession, page_object: EditUserModel):
    """
    编辑用户信息service
    :param query_db: orm对象
    :param page_object: 编辑用户对象
    :return: 编辑用户校验结果
    """
    edit_user = page_object.model_dump(exclude_unset=True, exclude={'admin'})
    user_info = await UserService.user_detail_services(query_db, edit_user.get('user_id'))
    if user_info.data and user_info.data.user_id:
        if page_object.type == 'user_name':
            if not await UserService.check_user_name_unique_services(query_db, page_object):
                    print('修改用户{page_object.user_name}失败，登录账号已存在')
                    return False      
        try:
            await UserDao.edit_user_dao(query_db, edit_user)
            await query_db.commit()
            return True
        except Exception as e:
            await query_db.rollback()
            return False
    else:
        return False




async def edit_system_user(
    edit_user: EditUserModel,
    query_db: AsyncSession
):
    edit_user.update_by = "system"
    edit_user.update_time = datetime.now()
    edit_user_result = await edit_user_services(query_db, edit_user)
    if edit_user_result:
        return True
    else:
        return False






async def edit_username_id(db: AsyncSession, user: schemas.User):
    edit_account = EditUserModel()
    edit_account.user_id = user.id
    edit_account.user_name = user.name
    edit_account.type = "use_rname"
    return await edit_system_user(edit_user=edit_account,query_db=db)
    # db.query(SysUser).filter_by(id=user.id).update({"name": user.name})
    # db.commit()

async def edit_pwd_id(db: AsyncSession, user: schemas.UserPwd):
    edit_account = EditUserModel()
    edit_account.user_id = user.id
    edit_account.password = PwdUtil.get_password_hash(user.password)
    edit_account.type = "pwd"
    return await edit_system_user(edit_user=edit_account,query_db=db)
    # db.query(SysUser).filter_by(id=user.id).update({"password":user.password})
    # db.commit()

    # # fake_hashed_password = user.password + "notreallyhashed"
    # db_user = models.User(name=user.name, password=fake_hashed_password)
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user

async def create_historyitem(db: AsyncSession, history: schemas.HistoryItemCreate):
    

    # db_item = models.History(image=history.image,
    #                          time=history.time,
    #                          location=history.location,
    #                          latlng=history.latlng,
    #                          reportid=history.reportid,
    #                          predlabel=history.predlabel,
    #                          predclass=history.predclass,
    #                          predscore=history.predscore )

    db.add(history)
    db.commit()
    db.refresh(history)
    return history

# async def clear_all_data(db: AsyncSession,tablename:str):
#     try:
#         if(tablename == "history"):
#             # 清空 History 表中的所有数据
#             db.execute(delete(models.History))
#             db.commit()
#             return {"message": "History表中的所有数据已清空"}
#         elif(tablename == "user"):
#             # 清空 User 表中的所有数据
#             db.execute(delete(models.User))
#             db.commit()
#             return {"message": "User表中的所有数据已清空"}
#         elif(tablename == "all"):
#             # 清空 History 表中的所有数据
#             db.execute(delete(models.History))
#             # 清空 User 表中的所有数据
#             db.execute(delete(models.User))
#             db.commit()
#             return {"message": "两张表中的所有数据已清空"}
    
#     except Exception as e:
#         db.rollback()  # 如果出现错误，回滚事务
#         return {"error": str(e)}
























# def get_user_by_name(db: AsyncSession, name: str):
#     return db.query(models.SysUser).filter(models.User.name == name).first()

# def get_user_by_id(db: AsyncSession, id: int):
#     return db.query(models.User).filter(models.User.id == id).first()    
    
# def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
    
# def create_user(db: AsyncSession, user: schemas.UserCreate):
#     # fake_hashed_password = user.password + "notreallyhashed"
#     fake_hashed_password = user.password
#     db_user = models.User(name=user.name, password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def edit_username_id(db: AsyncSession, user: schemas.User):
#     db.query(models.User).filter_by(id=user.id).update({"name": user.name})
#     db.commit()

# def edit_pwd_id(db: AsyncSession, user: schemas.UserInfo):
#     db.query(models.User).filter_by(id=user.id).update({"password":user.password})
#     db.commit()

#     # # fake_hashed_password = user.password + "notreallyhashed"
#     # db_user = models.User(name=user.name, password=fake_hashed_password)
#     # db.add(db_user)
#     # db.commit()
#     # db.refresh(db_user)
#     # return db_user

# def create_historyitem(db: AsyncSession, history: schemas.HistoryItemCreate):
    

#     # db_item = models.History(image=history.image,
#     #                          time=history.time,
#     #                          location=history.location,
#     #                          latlng=history.latlng,
#     #                          reportid=history.reportid,
#     #                          predlabel=history.predlabel,
#     #                          predclass=history.predclass,
#     #                          predscore=history.predscore )

#     db.add(history)
#     db.commit()
#     db.refresh(history)
#     return history

# def clear_all_data(db: AsyncSession,tablename:str):
#     try:
#         if(tablename == "history"):
#             # 清空 History 表中的所有数据
#             db.execute(delete(models.History))
#             db.commit()
#             return {"message": "History表中的所有数据已清空"}
#         elif(tablename == "user"):
#             # 清空 User 表中的所有数据
#             db.execute(delete(models.User))
#             db.commit()
#             return {"message": "User表中的所有数据已清空"}
#         elif(tablename == "all"):
#             # 清空 History 表中的所有数据
#             db.execute(delete(models.History))
#             # 清空 User 表中的所有数据
#             db.execute(delete(models.User))
#             db.commit()
#             return {"message": "两张表中的所有数据已清空"}
    
#     except Exception as e:
#         db.rollback()  # 如果出现错误，回滚事务
#         return {"error": str(e)}
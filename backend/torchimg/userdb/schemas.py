from typing import List, Optional,Literal,Generic, TypeVar
from pydantic import BaseModel,Field
from fastapi import UploadFile, File
import base64
import os
from pydantic.generics import GenericModel
from PIL import Image
from io import BytesIO

T = TypeVar("T")  # 泛型 T

# 通用响应模型
class BaseResponse(GenericModel, Generic[T]):
    code: int = 200
    msg: str = "操作成功"
    data: Optional[T] = None

    class Config:
        from_attributes = True
        orm_mode = True

class VueUser(BaseModel):
    id: int
    # items: List[Item] = []
    # 向 Pydantic 提供配置
    class Config:
        from_attributes = True
        orm_mode = True  # 启用 ORM 模式

class VueAllClass(BaseModel):
    type0: int
    type1: int
    type2: int
    type3: int
    type4: int
    allrecord:int
    currentuserrecord:int
    # items: List[Item] = []
    
    # 向 Pydantic 提供配置
    class Config:
        from_attributes = True
        orm_mode = True  # 启用 ORM 模式
    
class VueRecords(BaseModel):
    id: str
    user_name: str
    updatedAt: str
    location: str
    predclass: str
    # items: List[Item] = []
    
    # 向 Pydantic 提供配置
    class Config:
        from_attributes = True
        orm_mode = True  # 启用 ORM 模式






class Users(BaseModel):
    name: str
    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True  # 启用 ORM 模式
    
    
class UserCreate(Users):
    password: str

class UserBase(BaseModel):
    id: int
    # items: List[Item] = []
    
    # 向 Pydantic 提供配置
    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True  # 启用 ORM 模式

    
class User(Users):
    id: int
    # items: List[Item] = []
    
    # 向 Pydantic 提供配置
    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True  # 启用 ORM 模式

    @classmethod
    def from_sqlalchemy_model(cls, item):
        # 生成Pydantic模型
        return cls(
            id=item.user_id,
            name=item.user_name,
        )

class UsersList(BaseModel):
    users: List[User]


class UserInfo(Users):
    user_id: Optional[int] = Field(default=None, description='用户ID')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    user_name: Optional[str] = Field(default=None, description='用户账号')
    nick_name: Optional[str] = Field(default=None, description='用户昵称')
    email: Optional[str] = Field(default=None, description='用户邮箱')
    phonenumber: Optional[str] = Field(default=None, description='手机号码')
    sex: Optional[str] = Field(default='2', description='用户性别（0男 1女 2未知）')
    # password: str
    # items: List[Item] = []
    # 向 Pydantic 提供配置
    class Config:
        from_attributes = True
        populate_by_name = True  
        orm_mode = True  # 启用 ORM 模式

class UserCheck(User):
    checkinfo: bool  # 仅扩展字段，无需重复定义Config


class UserPwd(BaseModel):
    id: int
    password: str
        # 向 Pydantic 提供配置
    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True  # 启用 ORM 模式

class HistoryItemCreate(BaseModel):
    image: str
    time: str
    location: str
    lat: str
    lng: str
    reportid: str
    predlabel: str
    predclass: str
    predscore: str
    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True  # 启用 ORM 模式

class HistoryItem(HistoryItemCreate):
    imageid: str
    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True  # 启用 ORM 模式


class HistoryItemResponse(BaseModel):
    imageid: int
    image_base64: str  # BLOB转Base64
    time: str
    location: str
    lat: str
    lng: str
    reportid: int
    predlabel: str
    predclass: str
    predscore: float
    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True  # 启用 ORM 模式
    
    # @classmethod
    # def compress_and_encode_image(path):
    #     try:
    #         with Image.open(path) as img:
    #             # 限制最大宽度为800像素，保持纵横比
    #             max_width = 800
    #             if img.width > max_width:
    #                 ratio = max_width / float(img.width)
    #                 new_height = int((float(img.height) * float(ratio)))
    #                 img = img.resize((max_width, new_height), Image.ANTIALIAS)

    #             # 转为JPEG压缩格式写入内存
    #             buffer = BytesIO()
    #             img.convert("RGB").save(buffer, format="JPEG", quality=80)
    #             buffer.seek(0)
    #             return base64.b64encode(buffer.read()).decode('utf-8')
    #     except Exception as e:
    #         print(f"[警告] 图片处理失败: {path}，原因: {e}")
    #         return None



    @classmethod
    def from_sqlalchemy_model(cls, item):


        def compress_and_encode_image(path):
            try:
                with Image.open(path) as img:
                    # 限制最大宽度为800像素，保持纵横比
                    max_width = 800
                    if img.width > max_width:
                        ratio = max_width / float(img.width)
                        new_height = int(img.height * ratio)
                        img = img.resize((max_width, new_height), Image.LANCZOS)

                    # 转换为RGB以避免某些格式问题（如PNG带透明通道）
                    img = img.convert("RGB")

                    # 压缩为JPEG格式并写入内存缓冲区
                    buffer = BytesIO()
                    img.save(buffer, format="JPEG", quality=75)  # 质量可调
                    buffer.seek(0)

                    # 编码为 Base64 字符串
                    return base64.b64encode(buffer.read()).decode('utf-8')
            except Exception as e:
                print(f"[错误] 无法压缩图片 {path}: {e}")
                return None
        # 如果图片字段不为空，进行Base64编码
        # 定义默认的logo路径
        default_logo_path = "assets/logo.png"
        if item.image_base64:
            modified_path = item.image_base64.replace("/profileimg/", "record_img/")


            # 检查图片文件是否存在，如果存在则读取该文件，否则使用默认logo
            if os.path.exists(modified_path):
                file_path = modified_path
            elif os.path.exists(default_logo_path):
                file_path = default_logo_path
            else:
                print("Neither the specified image nor the default logo was found.")

            if file_path :
                image_base64 = compress_and_encode_image(file_path)
            else: 
                image_base64 = None
            if not image_base64:
                image_base64 = compress_and_encode_image(default_logo_path)

        #     # 读取文件并进行Base64编码
        #     try:
        #         with open(file_path, "rb") as img_file:
        #             image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        #     except Exception as e:
        #         print(f"Error encoding image {file_path}: {e}")
        # else:
        #     # 如果图片字段为空，使用默认logo的Base64编码
        #     try:
        #         with open(default_logo_path, "rb") as img_file:
        #             image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        #     except Exception as e:
        #         print(f"Error encoding default logo: {e}")
        #         image_base64 = None 
        #     # image_base64 = base64.b64encode(item.image).decode('utf-8')


        # 生成Pydantic模型
        return cls(
            imageid=item.imageid,
            image_base64=image_base64,
            time=item.time,
            location=item.location,
            lat=str(item.lat) if item.lat is not None else None,
            lng=str(item.lng) if item.lng is not None else None,
            reportid=item.reportid,
            predlabel=item.predlabel,
            predclass=item.predclass,
            predscore=item.predscore
        )
    


class PaginationMeta(BaseModel):
    current_page: int
    current_record: int
    page_size: int
    total_records: int
    total_pages: int
    has_next_page: bool
    class Config:
        from_attributes=True
        orm_mode = True  # 启用 ORM 模式


class PaginatedResponse(BaseModel):
    data: list[HistoryItemResponse]
    pagination: PaginationMeta


# @classmethod
# def from_sqlalchemy_model(cls, item):
#     # 如果图片字段不为空，进行Base64编码
#     image_base64 = None
#     if item.image:
#         image_base64 = base64.b64encode(item.image).decode('utf-8')
#     # 生成Pydantic模型
#     return cls(
#         id=item.id,
#         image_base64=image_base64,
#         time=item.time,
#         location=item.location,
#         lat=item.lat,
#         lng=item.lng,
#         report_id=item.report_id,
#         pred_label=item.pred_label,
#         pred_score=item.pred_score
#     )



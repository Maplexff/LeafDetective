# -*- coding:utf-8 -*-

from sqlalchemy import Column, ForeignKey, String, DateTime, BigInteger, Integer, LargeBinary, Float, Text
from config.database import BaseMixin, Base




class History(Base, BaseMixin):
    __tablename__ = "history"

    image = Column(String(200), nullable=False, comment='图像')

    lat = Column(Float, nullable=False, comment='纬度')

    lng = Column(Float, nullable=False, comment='经度')

    location = Column(Text, nullable=False, comment='地点')

    predclass = Column(Text, nullable=False, comment='预测类别')

    predlabel = Column(Text, nullable=False, comment='预测标签')

    predscore = Column(Float, nullable=False, comment='预测分数')

    reportid = Column(BigInteger, nullable=False, comment='上报ID')

    time = Column(Text, nullable=False, comment='时间')

    update_by = Column(String(64), comment='更新者')


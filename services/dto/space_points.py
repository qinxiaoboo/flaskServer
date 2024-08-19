from flaskServer.config.connect import app,db
from flaskServer.mode.space_points import SpacePoints
from sqlalchemy import and_
from loguru import  logger
# 获取银河任务点
def getSpacePoints(env,name,alia):
    with app.app_context():
        space = SpacePoints.query.filter(and_(SpacePoints.env_name==env,SpacePoints.name==name,SpacePoints.alia==alia)).first()
        return space
# 更新银河任务点
def updateSpacePoints(env_name,name,alia,points,ranking):
    space = getSpacePoints(env_name,name,alia)
    with app.app_context():
        if space:
            if space.points != points:
                space.points = points
            if space.ranking != ranking:
                space.ranking = ranking
            logger.info(f"{env_name}: 更新Galxe 数据")
        else:
            space = SpacePoints(env_name=env_name,name=name,alia=alia,points=points,ranking=ranking)
            logger.info(f"{env_name}: 新增Galxe 数据")
        db.session.add(space)
        db.session.commit()

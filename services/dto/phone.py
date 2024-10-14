from flaskServer.config.connect import db, app
from flaskServer.mode.phone import Phone

def getPhoneByName(name):
    with app.app_context():
        phone = Phone.query.filter_by(name=name).first()
        return phone

def updatePhone(country_code,name,country_id,request_id, status):
    phone = getPhoneByName(name)
    with app.app_context():
        if phone:
            if request_id and request_id != phone.requestId:
                phone.requestId = request_id
            if status and status != phone.status:
                phone.status = status
            if country_id and country_id != phone.country_id:
                phone.country_id = country_id
            if country_code and country_code != phone.country_code:
                phone.country_code = country_code
        else:
            phone = Phone(name=name, country_id=country_id, country_code=country_code, requestId=request_id, status=status)
        db.session.add(phone)
        db.session.commit()
        return phone
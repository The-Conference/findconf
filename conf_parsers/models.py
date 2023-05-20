from sqlalchemy import Column, Integer, String, Boolean, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates


Base = declarative_base()


class ConferenceItemDB(Base):
    __tablename__ = 'Conference_data_conference'

    id = Column(Integer, primary_key=True, index=True)
    conf_id = Column(String)
    hash = Column(String(500))
    un_name = Column(String(500))
    local = Column(Boolean, default=True)
    reg_date_begin = Column(Date, nullable=True)
    reg_date_end = Column(Date, nullable=True)
    conf_date_begin = Column(Date)
    conf_date_end = Column(Date)
    conf_card_href = Column(String(500))
    reg_href = Column(String(500), nullable=True)
    conf_name = Column(String)
    conf_s_desc = Column(String, nullable=True)
    conf_desc = Column(String, nullable=True)
    org_name = Column(String, nullable=True)
    themes = Column(String, nullable=True)
    online = Column(Boolean, default=False)
    conf_href = Column(String(500), nullable=True)
    offline = Column(Boolean, default=True)
    conf_address = Column(String, nullable=True)
    contacts = Column(String, nullable=True)
    rinc = Column(Boolean, default=False)
    data = Column(JSON, nullable=True)
    checked = Column(Boolean, default=False)
    generate_conf_id = Column(Boolean, default=False)
    vak = Column(Boolean, default=False)
    wos = Column(Boolean, default=False)
    scopus = Column(Boolean, default=False)

    @validates('hash', 'un_name', 'conf_card_href', 'reg_href', 'conf_href')
    def validate_code(self, key, value):
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            return value[:max_len]
        return value

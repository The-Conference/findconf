from sqlalchemy import Column, Integer, String, Boolean, Date, JSON, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates


Base = declarative_base()


class ConferenceItemDB(Base):
    __tablename__ = 'Conference_data_conference'

    id = Column(Integer, primary_key=True, index=True)
    conf_id = Column(String, unique=True, nullable=False)
    hash = Column(String(500), nullable=True)
    un_name = Column(String(500), nullable=False)
    local = Column(Boolean, default=True)
    reg_date_begin = Column(Date, nullable=True, default=null())
    reg_date_end = Column(Date, nullable=True, default=null())
    conf_date_begin = Column(Date, nullable=False)
    conf_date_end = Column(Date, nullable=True, default=null())
    conf_card_href = Column(String(500), default=null())
    reg_href = Column(String(500), nullable=True, default=null())
    conf_name = Column(String, nullable=False)
    conf_s_desc = Column(String, nullable=True, default=null())
    conf_desc = Column(String, nullable=False, default='')
    org_name = Column(String, nullable=True, default=null())
    themes = Column(String, nullable=True, default=null())
    online = Column(Boolean, default=False)
    conf_href = Column(String(500), nullable=True, default=null())
    offline = Column(Boolean, default=True)
    conf_address = Column(String, nullable=True, default=null())
    contacts = Column(String, nullable=True, default=null())
    rinc = Column(Boolean, default=False)
    data = Column(JSON, nullable=True, default=null())
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

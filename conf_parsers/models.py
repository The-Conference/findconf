from sqlalchemy import Column, Integer, String, Boolean, Date, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates


Base = declarative_base()


class ConferenceItemDB(Base):
    __tablename__ = 'Conference_data_conference'

    id = Column(Integer, primary_key=True, index=True, doc="Internal ID, automatically generated by the DB.")
    item_id = Column(String, unique=True, nullable=False,
                     doc="Actual ID. Generated by :func:`~conf_spiders.pipelines.FillTheBlanksPipeline`.")
    un_name = Column(String(500), nullable=False, doc="University name. Given in the spiders' properties.")
    local = Column(Boolean, default=True, doc="False in the conference is international. "
                                              "Parsed by :func:`~conf_spiders.pipelines.FillTheBlanksPipeline`.")
    reg_date_begin = Column(Date, nullable=True, default=null(), doc="Registration start date. Parsed.")
    reg_date_end = Column(Date, nullable=True, default=null(), doc="Registration end date. Parsed.")
    conf_date_begin = Column(Date, nullable=False, doc="Conference start date. Parsed.")
    conf_date_end = Column(Date, nullable=True, default=null(), doc="Conference end date. Parsed.")
    source_href = Column(String(500), default=null(), doc="Link to the conference page. Parsed.")
    reg_href = Column(String(500), nullable=True, default=null(), doc="Link to the registration form. Parsed.")
    title = Column(String, nullable=False, doc="Conference title. Parsed.")
    short_description = Column(String, nullable=True, default=null(),
                               doc="Conference short description. Mostly unused. Parsed.")
    description = Column(String, nullable=False, default='', doc="Conference full description. Parsed.")
    org_name = Column(String, nullable=True, default=null(), doc="Conference organisers. Field unused.")
    online = Column(Boolean, default=False, doc="True if the conference is accessible on the Internet. Parsed.")
    conf_href = Column(String(500), nullable=True, default=null(), doc="Dedicated website of the conference. Parsed.")
    offline = Column(Boolean, default=True, doc="False in conference is online-only. Parsed.")
    conf_address = Column(String, nullable=True, default=null(), doc="Conference address. Parsed.")
    contacts = Column(String, nullable=True, default=null(), doc="Organisers' contact data. Parsed.")
    rinc = Column(Boolean, default=False, doc="Citation database: Российский индекс научного цитирования. Parsed.")
    checked = Column(Boolean, default=False, doc="True if manually approved. Manually entered.")
    vak = Column(Boolean, default=False, doc="Citation database: Высшая Аттестационная Комиссия. Parsed.")
    wos = Column(Boolean, default=False, doc="Citation database: Web of Science. Parsed.")
    scopus = Column(Boolean, default=False, doc="Citation database: Elsevier. Parsed.")

    @validates('hash', 'un_name', 'source_href', 'reg_href', 'conf_href')
    def validate_code(self, key, value):
        """Automatically truncates field entries above max character limit."""
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            return value[:max_len]
        return value

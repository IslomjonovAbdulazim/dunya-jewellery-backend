from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    sizes = Column(Text)  # "16.5,17,17.5,18"
    telegram_file_ids = Column(Text)  # "file_id1,file_id2"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def get_sizes_list(self):
        """Return sizes as list of floats"""
        if not self.sizes:
            return []
        try:
            return [float(s.strip()) for s in self.sizes.split(",") if s.strip()]
        except:
            return []

    def get_file_ids_list(self):
        """Return file IDs as list"""
        if not self.telegram_file_ids:
            return []
        return [f.strip() for f in self.telegram_file_ids.split(",") if f.strip()]

    def set_sizes(self, sizes_list):
        """Set sizes from list"""
        if sizes_list:
            self.sizes = ",".join([str(s) for s in sizes_list])
        else:
            self.sizes = ""

    def set_file_ids(self, file_ids_list):
        """Set file IDs from list"""
        if file_ids_list:
            self.telegram_file_ids = ",".join(file_ids_list)
        else:
            self.telegram_file_ids = ""

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    telegram_username = Column(String(100))
    phone_numbers = Column(Text)  # "phone1,phone2,phone3"
    instagram_username = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def get_phone_numbers_list(self):
        """Return phone numbers as list"""
        if not self.phone_numbers:
            return []
        return [p.strip() for p in self.phone_numbers.split(",") if p.strip()]

    def set_phone_numbers(self, phone_list):
        """Set phone numbers from list"""
        if phone_list:
            self.phone_numbers = ",".join([str(p) for p in phone_list])
        else:
            self.phone_numbers = ""
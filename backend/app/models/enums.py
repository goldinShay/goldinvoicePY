from enum import Enum

class ContactType(str, Enum):
    PERSONAL = "PERSONAL"
    BUSINESS = "BUSINESS"
    FREELANCE = "FREELANCE"

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    CHF = "CHF"
    JPY = "JPY"

class Language(str, Enum):
    ENGLISH = "ENGLISH"
    DUTCH = "DUTCH"
    HEBREW = "HEBREW"
    FRENCH = "FRENCH"
    GERMAN = "GERMAN"
    SPANISH = "SPANISH"

class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

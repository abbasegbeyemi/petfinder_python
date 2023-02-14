import enum


class Distance(enum.Enum):
    """
    The distance from the location to search for pets.
    """
    FIFTY_MILES = 80
    SEVENTY_FIVE_MILES = 121


class AgeRange(enum.Enum):
    """
    The age range of the pets to search for.
    Kitten: 0-3 months
    Juvenile: 4-12 months
    """
    KITTEN = 1
    JUVENILE = 2


class AdvertiserType(enum.Enum):
    """
    The type of advertiser to search for.
    """
    INDIVIDUAL = "individual"
    BREEDER = "breeder"
    RESCUE_CHARITY = "rescue-charity"

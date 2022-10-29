from typing import Dict, List, OrderedDict
from CTFd.models import Users, db
from CTFd.utils.countries import COUNTRIES_DICT, lookup_country_code

# Be explicit: make it easy to reason the code
# Less coupling: reduce risks for breaking changes from upstream


# Weak Entity On Users
class CSAWMembers(db.Model):
    __tablename__ = "csaw_members"

    # fields
    sub_id = db.Column(db.Integer, primary_key=True)  # 0,1,2,3
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    school = db.Column(db.String(128))

    def asdict(self) -> Dict:
        result = {
            "sub_id": self.sub_id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "school": self.school,
        }
        return result

    @classmethod
    def fromdict(cls, d):
        member = cls()

        member.sub_id = d.sub_id
        member.user_id = d.user_id
        member.name = d.name
        member.email = d.email
        member.school = d.school

        return member


class CSAWRegions(db.Model):
    __tablename__ = "csaw_regions"

    country = db.Column(db.String(128), primary_key=True)
    region = db.Column(db.String(128))

    @property
    def country_name(self) -> str:
        return lookup_country_code(self.country)

    def asdict(self) -> Dict:
        result = {
            "country": self.country,
            "region": self.region,
        }
        return result

    @classmethod
    def fromdict(cls, d):
        region = cls()

        region.country = d.country
        region.region = d.region

        return region


def get_members(user: Users) -> List[CSAWMembers]:
    members = CSAWMembers.query.filter_by(user_id=user.id).order_by(CSAWMembers.sub_id)
    result = members.all()
    return result


def get_region(country: str) -> str:
    query_obj = CSAWRegions.query.get(country)
    region = query_obj.region
    return region


def get_country_region_dict() -> OrderedDict:
    query_obj = CSAWRegions.query.all()
    result = OrderedDict([(q.country, q.region) for q in query_obj])
    return result


def update_country_region(country: str, region: str):
    # wrong country
    if country not in COUNTRIES_DICT:
        raise ValueError(f"Country {country} does not exist")

    try:
        # existing country
        query_obj = CSAWRegions.query.get(country)
    except:
        # new country
        query_obj = CSAWRegions()
        query_obj.country = country

    query_obj.region = region

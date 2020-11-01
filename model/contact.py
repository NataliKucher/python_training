from sys import maxsize


class Contact:
    def __init__(self, firstname=None, middlename=None, lastname=None, nickname=None, id=None, company=None,
                 address=None, homephone=None, mobilephone=None, workphone=None,
                 secondaryphone=None, all_email=None, all_phones_from_home_page=None, email=None, email2=None,
                 homepage=None, address2=None):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.nickname = nickname
        self.id = id
        self.company = company
        self.address = address
        self.homephone = homephone
        self.mobilephone = mobilephone
        self.workphone = workphone
        self.secondaryphone = secondaryphone
        self.all_phones_from_home_page = all_phones_from_home_page
        self.all_email = all_email
        self.email = email
        self.email2 = email2
        self.homepage = homepage
        self.address2 = address2

    def __repr__(self):
        return "{0}:{1} {2}".format(self.id, self.firstname, self.lastname)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) \
               and self.firstname == other.firstname and self.lastname == other.lastname

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize

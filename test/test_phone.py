import re
from fixture.contact import Contact
import pytest


def test_add_new(app, json_contacts):
    new_contact = json_contacts
    old_contacts = app.contact.get_contact_list()
    app.contact.create(new_contact)
    assert len(old_contacts) + 1 == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(new_contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)


def test_phones_on_home_page(app):
    contact_from_home_page = app.contact.get_contact_list()[0]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)


def test_phones_on_contact_view_page(app):
    contact_from_view_page = app.contact.get_contact_from_view_page(0)
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert contact_from_view_page.homephone == contact_from_edit_page.homephone
    assert contact_from_view_page.workphone == contact_from_edit_page.workphone
    assert contact_from_view_page.mobilephone == contact_from_edit_page.mobilephone
    assert contact_from_view_page.secondaryphone == contact_from_edit_page.secondaryphone


# def test_full_data_on_home_page(app):
#     full_data_from_home_page = app.contact.get_contact_list()[0]
#     full_data_contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
#     # assert full_data_from_home_page == merge_data_like_on_home_page(full_data_contact_from_edit_page)
#
# #
# def test_full_data_on_contact_view_page(app):
#     contact_from_view_page = app.contact.get_contact_from_view_page(0)
#     contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
#     assert contact_from_view_page.firstname == contact_from_edit_page.firstname
#     assert contact_from_view_page.middlename == contact_from_edit_page.middlename
#     assert contact_from_view_page.lastname == contact_from_edit_page.lastname
#     assert contact_from_view_page.homephone == contact_from_edit_page.homephone
#     assert contact_from_view_page.workphone == contact_from_edit_page.workphone
#     assert contact_from_view_page.mobilephone == contact_from_edit_page.mobilephone
#     assert contact_from_view_page.secondaryphone == contact_from_edit_page.secondaryphone


def clear(s):
    return re.sub("[() -]", "", s)  # замена шаблона на подст. в строке


def merge_phones_like_on_home_page(contact):
    # обратная проверка->строчки склеили
    return "\n".join(filter(lambda x: x != "",
                            map(lambda x: clear(x),
                                filter(lambda x: x is not None,
                                       [contact.homephone, contact.mobilephone,
                                        contact.workphone,
                                        contact.secondaryphone]))))

    #  filter(lambda x: x is not None,т.к нельзя применят' позже clear если есть не пустые строки "", а None

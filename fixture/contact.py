from model.contact import Contact
import re


class ContactHelper:
    def __init__(self, app):
        self.app = app

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.app.open_home_page()
            self.contact_cache = []
            for row in wd.find_elements_by_xpath('//tr[@name="entry"]'):
                cells = row.find_elements_by_tag_name("td")
                id = cells[0].find_element_by_name("selected[]").get_attribute("value")
                lastname = cells[1].text
                firstname = cells[2].text
                address = cells[3].text
                all_email = cells[4].text
                all_phones = cells[5].text  # +порезать .splitlines() прямая проверка
                self.contact_cache.append(Contact(firstname=firstname, lastname=lastname, id=id, address=address,
                                                  all_email=all_email, all_phones_from_home_page=all_phones))
        return list(self.contact_cache)  # (скопировано из документа класса)

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        phones = wd.find_element_by_id("content").text
        homephone = re.search("H: (.*)", phones).group(1)
        workphone = re.search("W: (.*)", phones).group(1)
        mobilephone = re.search("M: (.*)", phones).group(1)
        secondaryphone = re.search("P: (.*)", phones).group(1)

        full_name = wd.find_element_by_xpath("//div[@id='content']/b").text
        firstname = re.split(" ", full_name)[0]
        middlename = re.split(" ", full_name)[1]
        lastname = re.split(" ", full_name)[2]

        nickname = wd.find_element_by_xpath("//div[@id='content']/br[1]").text
        company = wd.find_element_by_xpath("//div[@id='content']/br[2]").text
        address = wd.find_element_by_xpath("//div[@id='content']/br[3]").text
        return Contact(firstname=firstname, middlename=middlename, lastname=lastname, nickname=nickname,
                       company=company, address=address,
                       homephone=homephone, mobilephone=mobilephone, workphone=workphone, secondaryphone=secondaryphone)

    def get_contact_info_from_edit_page(self, index):
        self.open_contact_to_edit_by_index(index)
        wd = self.app.wd
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        middlename = wd.find_element_by_name("middlename").get_attribute("value")
        nickname = wd.find_element_by_name("nickname").get_attribute("value")

        address = wd.find_element_by_name("address").get_attribute("value")
        address2 = wd.find_element_by_name("address2").get_attribute("value")
        company = wd.find_element_by_name("company").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        homepage = wd.find_element_by_name("homepage").get_attribute("value")

        homephone = wd.find_element_by_name("home").get_attribute("value")
        mobilephone = wd.find_element_by_name("mobile").get_attribute("value")
        workphone = wd.find_element_by_name("work").get_attribute("value")
        secondaryphone = wd.find_element_by_name("phone2").get_attribute("value")

        id = wd.find_element_by_name("id").get_attribute("value")
        return Contact(firstname=firstname, middlename=middlename, lastname=lastname, nickname=nickname,
                       company=company, address=address, address2=address2,
                       homephone=homephone, mobilephone=mobilephone, workphone=workphone, secondaryphone=secondaryphone,
                       homepage=homepage, email=email, email2=email2, id=id)

    def fill_group_form(self, contact):
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("middlename", contact.middlename)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("nickname", contact.nickname)
        self.change_field_value("address", contact.address)
        self.change_field_value("home", contact.homephone)
        self.change_field_value("company", contact.company)
        self.change_field_value("mobile", contact.mobilephone)
        self.change_field_value("work", contact.workphone)
        self.change_field_value("homepage", contact.homepage)
        self.change_field_value("email2", contact.email2)
        self.change_field_value("email", contact.email)
        self.change_field_value("phone2", contact.secondaryphone)
        self.change_field_value("address2", contact.address2)

    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_xpath('//tr[@name="entry"]')[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        row = wd.find_elements_by_xpath('//tr[@name="entry"]')[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def create(self, contact):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()
        self.fill_group_form(contact)
        wd.find_element_by_xpath("(//input[@name='submit'])[2]").click()
        self.app.open_home_page()
        self.contact_cache = None

    def count(self):
        wd = self.app.wd
        self.app.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    #
    # def return_to_home_page(self):
    #     wd = self.app.wd
    #     wd.find_element_by_link_text("home").click()
    #
    # def return_to_add_new_user(self):
    #     wd = self.app.wd
    #     wd.find_element_by_link_text("add new").click()

    # def select_first_user(self):
    #     self.select_user_by_index(0)
    #
    # def select_user_by_index(self, index):
    #     wd = self.app.wd
    #     wd.find_elements_by_name("selected[]")[index].click()
    #
    # def modify_user(self, new_user_data, index):
    #     wd = self.app.wd
    #     self.return_to_home_page()
    #     self.select_user_by_index(index)
    #     # open modification form
    #     wd.find_element_by_xpath('//img[@title="Edit"]').click()
    #     self.fill_group_form(new_user_data)
    #     # submit modification
    #     wd.find_element_by_name("update").click()
    #     self.return_to_home_page()
    #     self.user_cache = None
    #
    # def modify_first_user(self, new_user_data):
    #     self.modify_user(new_user_data, 0)
    #
    # def delete_user(self, index):
    #     wd = self.app.wd
    #     self.return_to_home_page()
    #     self.select_user_by_index(index)
    #     wd.find_element_by_xpath('//img[@title="Edit"]').click()
    #     wd.find_element_by_xpath('//input[@value="Delete"]').click()
    #     self.return_to_home_page()
    #     self.user_cache = None

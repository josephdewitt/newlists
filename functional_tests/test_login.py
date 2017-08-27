from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time
from contextlib import contextmanager

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):


    def test_can_get_email_link_to_Log_in(self):
        # Joseph goes to the awesone superlist site
        # and notices a "log in" section in the mavbar for the first time
        # It's telling her to enter her email address, so she does
        print('THIS IS THE ONE: %s' % self.staging_server)

        if self.staging_server:
            test_email = 'joseph@jpsenior.com'
        else:
            test_email = 'edith@example.com'


        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        #a message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn('Check your email', self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail('could not find url in email body: \n %s' % body)
        url  = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        #she is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)

    # def wait_for_email(self, test_email, subject):
    #     if not self.staging_server:
    #         email = mail.outbox[0]
    #         self.assertIn(test_email, email.to)
    #         self.assertEqual(email.subject, subject)
    #         return email.body
    #
    #     email_id = None
    #     start = time.time()
    #     inbox = poplib.POP3_SSL('mail.jpsenior.com')
    #     try:
    #         inbox.user('joseph')
    #         inbox.pass_(os.environ['YAHOO_PASSWORD'])
    #
    #         while time.time() - start < 60:
    #             get 10 newest messages
                # count, _ = inbox.stat()
                # for i in reversed(range(max(1, count - 10), count + 1)):
                #     print('getting msg', i)
                #     _, lines, __ = inbox.retr(i)
                #     lines = [l.decode('utf8') for l in lines]
                #     print(lines)
                #     if 'Subject: %s' % subject in lines:
                #         email_id = i
                #         body = '\n'.join(lines)
                #         return body
                # time.sleep(5)
        # finally:
        #     if email_id:
        #         inbox.dele(email_id)
        #     inbox.quit()

    @contextmanager
    def pop_inbox(self):
        try:
            inbox = poplib.POP3_SSL('mail.jpsenior.com')
            inbox.user('joseph')
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            yield inbox

        finally:
            inbox.quit()

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(subject, email.subject)
            return email.body

        last_count = 0
        start = time.time()

        while time.time() - start < 60:
            with self.pop_inbox() as inbox:
                count, _ = inbox.stat()
                if count != last_count:
                    for i in range(count, last_count, -1):
                        _, lines, __ = inbox.retr(i)
                        lines = [l.decode('utf8') for l in lines]
                        if 'Subject: %s'  % subject in lines:
                            inbox.dele(i)
                            return '\n'.join(lines)
                    last_count = count
            time.sleep(5)
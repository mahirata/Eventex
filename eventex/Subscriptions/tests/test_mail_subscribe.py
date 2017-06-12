from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Marco Hirata', cpf='12345678901', email='marco.hirata@gmail.com', phone='11-98730-0315')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEquals(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEquals(expect, self.email.from_email)

    def test_subscription_email_body(self):
        expect = ['contato@eventex.com.br', 'marco.hirata@gmail.com']
        self.assertEquals(expect, self.email.to)

    def test_subscription_email_to(self):
        contents = [
            'Marco Hirata',
            '12345678901',
            'marco.hirata@gmail.com',
            '11-98730-0315',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

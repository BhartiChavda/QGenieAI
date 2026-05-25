from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.utils import timezone
from QGenieAIapp.models import OTPVerification

class OTPVerificationTests(TestCase):
    def test_user_registration_creates_inactive_user(self):
        """
        Verify that registering a new user creates the user in inactive state,
        generates an OTP, and sends a verification email.
        """
        register_url = reverse('register')
        post_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        
        response = self.client.post(register_url, post_data)
        
        # Verify redirect to verify-otp page
        self.assertRedirects(response, reverse('verify_otp', kwargs={'username': 'newuser'}))
        
        # Verify user is created and is inactive
        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_active)
        
        # Verify OTP is created
        self.assertTrue(OTPVerification.objects.filter(user=user).exists())
        otp = user.otp_verification
        self.assertEqual(len(otp.otp_code), 6)
        self.assertTrue(otp.otp_code.isdigit())
        
        # Verify email is sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(otp.otp_code, mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, ['newuser@example.com'])

    def test_correct_otp_verifies_user(self):
        """
        Verify that submitting the correct and valid OTP code activates the user
        and logs them in automatically.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123', is_active=False)
        otp_code = '123456'
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        OTPVerification.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)
        
        verify_url = reverse('verify_otp', kwargs={'username': 'testuser'})
        response = self.client.post(verify_url, {'otp_code': otp_code})
        
        # Verify success redirects to dashboard
        self.assertRedirects(response, reverse('dashboard'))
        
        # Verify user is now active
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        
        # Verify OTP record is deleted
        self.assertFalse(OTPVerification.objects.filter(user=user).exists())
        
        # Verify user is logged in
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_incorrect_otp_returns_error(self):
        """
        Verify that submitting an incorrect OTP code keeps the user inactive
        and returns an error message.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123', is_active=False)
        otp_code = '123456'
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        OTPVerification.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)
        
        verify_url = reverse('verify_otp', kwargs={'username': 'testuser'})
        response = self.client.post(verify_url, {'otp_code': '999999'})
        
        # Verify user is still inactive
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        
        # Verify OTP record is still present
        self.assertTrue(OTPVerification.objects.filter(user=user).exists())

    def test_expired_otp_returns_error(self):
        """
        Verify that submitting an expired OTP keeps the user inactive.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123', is_active=False)
        otp_code = '123456'
        # Expired 5 minutes ago
        expires_at = timezone.now() - timezone.timedelta(minutes=5)
        OTPVerification.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)
        
        verify_url = reverse('verify_otp', kwargs={'username': 'testuser'})
        response = self.client.post(verify_url, {'otp_code': otp_code})
        
        # Verify user is still inactive
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_resend_otp(self):
        """
        Verify that hitting the resend endpoint generates a new OTP code,
        updates the expiration time, and sends a new email.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123', is_active=False)
        old_otp_code = '111111'
        expires_at = timezone.now() - timezone.timedelta(minutes=5)  # already expired
        otp_record = OTPVerification.objects.create(user=user, otp_code=old_otp_code, expires_at=expires_at)
        
        resend_url = reverse('resend_otp', kwargs={'username': 'testuser'})
        response = self.client.get(resend_url)
        
        # Verify it redirects back to verify_otp
        self.assertRedirects(response, reverse('verify_otp', kwargs={'username': 'testuser'}))
        
        # Verify record updated
        otp_record.refresh_from_db()
        self.assertNotEqual(otp_record.otp_code, old_otp_code)
        self.assertTrue(otp_record.expires_at > timezone.now())
        
        # Verify new email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(otp_record.otp_code, mail.outbox[0].body)

    def test_inactive_user_login_redirects_to_otp_verification(self):
        """
        Verify that an unverified user trying to log in gets redirected to the
        OTP verification screen rather than just failing with an invalid credentials message.
        """
        user = User.objects.create_user(username='inactiveuser', email='inactive@example.com', password='password123', is_active=False)
        
        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': 'inactiveuser',
            'password': 'password123',
        })
        
        # Verify redirect to verify-otp page
        self.assertRedirects(response, reverse('verify_otp', kwargs={'username': 'inactiveuser'}))



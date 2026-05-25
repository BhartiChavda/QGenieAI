from django.urls import path
from . import views

urlpatterns = [
    # --- User Authentication ---
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-otp/<str:username>/', views.verify_otp_view, name='verify_otp'),
    path('verify-otp/<str:username>/resend/', views.resend_otp_view, name='resend_otp'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password-verify/<str:username>/', views.forgot_password_verify_view, name='forgot_password_verify'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/verify-email/', views.verify_email_change_view, name='verify_email_change'),
    path('profile/verify-password-reset/', views.profile_verify_password_reset_view, name='profile_verify_password_reset'),


    
    # --- Core Web App User Panel ---
    path('', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_view, name='upload'),
    path('quiz/<int:file_id>/', views.quiz_view, name='quiz'),
    path('review/<int:file_id>/', views.review_content_view, name='review_content'),
    path('review/<int:file_id>/add-question/', views.add_custom_question_view, name='add_custom_question'),
    path('preview/<int:file_id>/', views.file_preview_view, name='file_preview'),
    path('result/', views.result_view, name='submit_quiz'),
    path('result/<int:result_id>/', views.result_view, name='quiz_result'),
    path('history/', views.history_view, name='history'),
    
    # Advanced QGenie AI Features
    path('chat/<int:file_id>/', views.chat_with_pdf_view, name='chat_with_pdf'),
    path('summary/<int:file_id>/', views.summary_view, name='summary'),
    path('download/<int:file_id>/<str:format_type>/', views.download_content_view, name='download_content'),

    # --- Custom Administrative Panel ---
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # User Management
    path('admin-panel/users/', views.admin_manage_users_view, name='admin_manage_users'),
    path('admin-panel/users/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('admin-panel/users/toggle/<int:user_id>/', views.admin_toggle_user_view, name='admin_toggle_user'),
    path('admin-panel/users/delete/<int:user_id>/', views.admin_delete_user_view, name='admin_delete_user'),
    
    # File/Uploads Management
    path('admin-panel/files/', views.admin_manage_files_view, name='admin_manage_files'),
    path('admin-panel/files/delete/<int:file_id>/', views.admin_delete_file_view, name='admin_delete_file'),
    
    # Generated Questions Management
    path('admin-panel/questions/', views.admin_manage_questions_view, name='admin_manage_questions'),
    path('admin-panel/questions/delete/<int:question_id>/', views.admin_delete_question_view, name='admin_delete_question'),
    path('admin-panel/questions/delete-normal/<int:question_id>/', views.admin_delete_normal_question_view, name='admin_delete_normal_question'),
    
    # Quiz Results Management
    path('admin-panel/results/', views.admin_manage_results_view, name='admin_manage_results'),
    path('admin-panel/results/delete/<int:result_id>/', views.admin_delete_result_view, name='admin_delete_result'),
]

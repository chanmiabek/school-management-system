from django.urls import path
from . import views

urlpatterns = [
   path('',views.index, name="index"),
   path('dashboard/', views.dashboard, name='dashboard'), 
   path('notification/mark_notification_as_read/', views.mark_notification_as_read, name='mark_notification_as_read' ),
   path('notification/clear_all_notifiaction/', views.clear_all_notification, name= "clear_all_notification"),

   path('teacher-dashboard/', views.app_page, {'page_title': 'Teacher Dashboard', 'page_description': 'Teacher dashboard module for Maggiso Programming Tech System.'}, name='teacher_dashboard'),
   path('profile/', views.profile_page, name='profile'),
   path('inbox/', views.inbox_page, name='inbox'),

   path('teachers/', views.teacher_list, name='teacher_list'),
   path('teachers/view/<int:teacher_id>/', views.teacher_view, name='teacher_view'),
   path('teachers/add/', views.add_teacher, name='add_teacher'),
   path('teachers/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),

   path('departments/', views.department_list, name='department_list'),
   path('departments/add/', views.add_department, name='add_department'),
   path('departments/edit/<int:department_id>/', views.edit_department, name='edit_department'),

   path('subjects/', views.subject_list, name='subject_list'),
   path('subjects/add/', views.add_subject, name='add_subject'),
   path('subjects/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),

   path('accounts/fees-collections/', views.fees_collection, name='fees_collection'),
   path('accounts/expenses/', views.expenses, name='expenses'),
   path('accounts/salary/', views.salary, name='salary'),
   path('accounts/add-fees/', views.add_fees, name='add_fees'),
   path('accounts/add-expenses/', views.add_expenses, name='add_expenses'),
   path('accounts/add-salary/', views.add_salary, name='add_salary'),

   path('holiday/', views.holiday_list, name='holiday'),
   path('holiday/add/', views.add_holiday, name='add_holiday'),
   path('fees/', views.fee_structure_list, name='fees'),
   path('fees/add/', views.add_fee_structure, name='add_fee_structure'),
   path('exam/', views.exam_list, name='exam_list'),
   path('exam/add/', views.add_exam, name='add_exam'),
   path('event/', views.event_list, name='events'),
   path('event/add/', views.add_event, name='add_event'),
   path('time-table/', views.time_table_list, name='time_table'),
   path('time-table/add/', views.add_time_table_entry, name='add_time_table_entry'),
   path('library/', views.library_list, name='library'),
   path('library/add/', views.add_library_book, name='add_library_book'),

   path('error-page/', views.app_page, {'page_title': 'Error Page', 'page_description': 'Error page preview.'}, name='error_page'),
   path('blank-page/', views.app_page, {'page_title': 'Blank Page', 'page_description': 'Reusable blank layout page.'}, name='blank_page'),
   path('sports/', views.sports_list, name='sports'),
   path('sports/add/', views.add_sport, name='add_sport'),
   path('hostel/', views.hostel_list, name='hostel'),
   path('hostel/add/', views.add_hostel_record, name='add_hostel_record'),
   path('transport/', views.transport_list, name='transport'),
   path('transport/add/', views.add_transport_route, name='add_transport_route'),
   path('components/', views.app_page, {'page_title': 'Components', 'page_description': 'UI components reference page.'}, name='components'),

   path('forms/basic-inputs/', views.app_page, {'page_title': 'Basic Inputs', 'page_description': 'Form basic input examples.'}, name='form_basic_inputs'),
   path('forms/input-groups/', views.app_page, {'page_title': 'Input Groups', 'page_description': 'Form input group examples.'}, name='form_input_groups'),
   path('forms/horizontal/', views.app_page, {'page_title': 'Horizontal Form', 'page_description': 'Horizontal form layout examples.'}, name='form_horizontal'),
   path('forms/vertical/', views.app_page, {'page_title': 'Vertical Form', 'page_description': 'Vertical form layout examples.'}, name='form_vertical'),
   path('forms/mask/', views.app_page, {'page_title': 'Form Mask', 'page_description': 'Form mask examples.'}, name='form_mask'),
   path('forms/validation/', views.app_page, {'page_title': 'Form Validation', 'page_description': 'Form validation examples.'}, name='form_validation'),

   path('tables/basic/', views.app_page, {'page_title': 'Basic Tables', 'page_description': 'Basic table examples.'}, name='tables_basic'),
   path('tables/data/', views.app_page, {'page_title': 'Data Table', 'page_description': 'Data table examples.'}, name='data_tables'),


]

from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('attempt/<int:id>',views.attempt_test,name="attempt_test"),
    path('save_response',views.save_response,name="save_response"),
    path('create_test',views.create_test,name="create_test"),
    path('create_question',views.create_test_from_json,name="create_question"),
    path('submit_test/<int:test_id>',views.submit_test,name="submit_test"),
    path('test_analysis/<int:test_id>',views.analyse,name="analyse")
]
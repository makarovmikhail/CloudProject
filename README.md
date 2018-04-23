Grid&Cloud course project

To execute project you need:
1) RabbitMQ Started on localhost by command: rabbitmqctl.bat list_queues
2) N ComputeCenters started by: python receive.py
3) webinterface - django app, started on: http://localhost:8000/webinterface/ by command: python manage.py runserver
4) admin - django app, automatically started on: http://localhost:8000/admin/ after step 3)

When you are visiting this page: http://localhost:8000/webinterface/
you have an opportunity to add some tasks using html form, and view 10 latest tasks with results.
After your task was added one of ComputeCenter solve it and then results will be updated.
Administrator can redact tasks visiting this page: http://localhost:8000/admin/

# Grid&Cloud course project

To execute project you need:
1) RabbitMQ Started on localhost by command: <b>rabbitmq-service start</b>
2) N ComputeCenters started by: <b>python receive.py</b>
3) webinterface - django app, started on: http://localhost:8000/webinterface/ by command: <b>python manage.py runserver</b>
4) admin - django app, automatically started on: http://localhost:8000/admin/ after step 3)

When you are visiting this page: http://localhost:8000/webinterface/
you have an opportunity to add some tasks using html form, and view 10 latest tasks with results.
After your task was added one of ComputeCenter solve it and then results will be updated.
Administrator can edit tasks visiting this page: http://localhost:8000/admin/

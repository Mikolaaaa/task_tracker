from rest_framework import generics
from .models import Status, User, User_Task, Task, Status_Task
from .serializers import StatusSerializer, Status_TaskSerializer, UserSerializer, User_TaskSerializer, TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError



# Список статусов
class status_list(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


# Добавить статус
@api_view(["POST"])
def create_status(request):
    if request.method == "POST":
        # Получение данных из тела запроса
        data = request.data
        try:
            # Создаем экземпляр модели на основе данных
            new_status = Status(name=data["name"], description=data["description"])
            new_status.full_clean()  # Выполняем валидацию
            new_status.save()  # Сохраняем объект, если валидация прошла успешно
        except ValidationError as e:
            return Response({"status": "error", "message": str(e)}, status=400)

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно создана"}, status=201)
    else:
        # Возвращаем ошибку, если запрос не методом POST
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["PUT"])
def update_status(request, id):
    if request.method == "PUT":
        # Получение данных из тела запроса
        data = request.data
        # Получение объекта Task по его идентификатору (id)
        status = get_object_or_404(Status, id=id)

        # Обновление значений полей, если они переданы в запросе
        if "name" in data:
            status.name = data["name"]
        if "description" in data:
            status.description = data["description"]

        try:
            # Создаем экземпляр модели на основе данных
            status.full_clean()  # Выполняем валидацию
            status.save()  # Сохраняем объект, если валидация прошла успешно
        except ValidationError as e:
            return Response({"status": "error", "message": str(e)}, status=400)

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно обновлена"})

    else:
        # Возвращаем ошибку, если запрос не методом PUT
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["DELETE"])
def delete_stasus(request, id):
    if request.method == "DELETE":
        # Получение объекта User_Task по его идентификатору (pk)
        status = get_object_or_404(Status, id=id)

        # Удаление объекта из базы данных
        status.delete()

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно удалена"})
    else:
        # Возвращаем ошибку, если запрос не методом DELETE
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


# Список связок статус/задача
class status_task_list(generics.ListCreateAPIView):
    queryset = Status_Task.objects.all()
    serializer_class = Status_TaskSerializer


# Добавить связку статус/задача
@api_view(["POST"])
def create_task_status(request):
    if request.method == "POST":
        # Получение данных из тела запроса
        data = request.data
        status = get_object_or_404(Status, id=request.data["status_id"])
        task = get_object_or_404(Task, id=request.data["task_id"])
        # Создание новой записи с использованием полученных данных
        new_record = Status_Task.objects.create(status_id=status, task_id=task)
        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно создана"}, status=201)
    else:
        # Возвращаем ошибку, если запрос не методом POST
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["PUT"])
def update_task_status(request, id):
    if request.method == "PUT":
        # Получение данных из тела запроса
        data = request.data
        # Получение объекта Task по его идентификатору (id)
        task_status = get_object_or_404(Status_Task, id=id)

        # Обновление значений полей, если они переданы в запросе
        if "status_id" in data:
            status = get_object_or_404(Status, id=request.data["status_id"])
            task_status.status_id = status
        if "task_id" in data:
            task = get_object_or_404(Task, id=request.data["task_id"])
            task_status.task_id = task

        # Сохранение обновленной записи
        task_status.save()

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно обновлена"})

    else:
        # Возвращаем ошибку, если запрос не методом PUT
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["DELETE"])
def delete_stasus_task(request, id):
    if request.method == "DELETE":
        # Получение объекта User_Task по его идентификатору (pk)
        status_task = get_object_or_404(Status_Task, id=id)

        # Удаление объекта из базы данных
        status_task.delete()

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно удалена"})
    else:
        # Возвращаем ошибку, если запрос не методом DELETE
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


# Список связкок пользователь/задача
class user_task_list(generics.ListCreateAPIView):
    queryset = User_Task.objects.all()
    serializer_class = User_TaskSerializer


# Добавить связку пользователь/задача
@api_view(["POST"])
def create_task_user(request):
    if request.method == "POST":
        # Получение данных из тела запроса
        data = request.data
        user = get_object_or_404(User, id=request.data["worker_id"])
        task = get_object_or_404(Task, id=request.data["task_id"])
        # Создание новой записи с использованием полученных данных
        new_record = User_Task.objects.create(worker_id=user, task_id=task)
        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно создана"}, status=201)
    else:
        # Возвращаем ошибку, если запрос не методом POST
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["PUT"])
def update_user_task(request, id):
    if request.method == "PUT":
        # Получение данных из тела запроса
        data = request.data
        # Получение объекта Task по его идентификатору (id)
        user_task = get_object_or_404(User_Task, id=id)

        # Обновление значений полей, если они переданы в запросе
        if "worker_id" in data:
            worker = get_object_or_404(User, id=request.data["worker_id"])
            user_task.worker_id = worker
        if "task_id" in data:
            task = get_object_or_404(Task, id=request.data["task_id"])
            user_task.task_id = task

        # Сохранение обновленной записи
        user_task.save()

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно обновлена"})

    else:
        # Возвращаем ошибку, если запрос не методом PUT
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["DELETE"])
def delete_user_task(request, id):
    if request.method == "DELETE":
        # Получение объекта User_Task по его идентификатору (pk)
        user_task = get_object_or_404(User_Task, id=id)

        # Удаление объекта из базы данных
        user_task.delete()

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно удалена"})
    else:
        # Возвращаем ошибку, если запрос не методом DELETE
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


# Список пользователей
class user_list(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Пользователь
class UserList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        # Получаем id пользователя из URL запроса
        id = self.kwargs['id']
        # Фильтруем задачи по пользователю
        queryset = User.objects.filter(id=id)
        return queryset


# Добавить пользователя
@api_view(["POST"])
def create_user(request):
    if request.method == "POST":
        # Получение данных из тела запроса
        data = request.data
        try:
            # Создаем экземпляр модели на основе данных
            new_user = User(name=data["name"], surname=data["surname"], patronymic=data["patronymic"], email=data["email"])
            new_user.full_clean()  # Выполняем валидацию
            new_user.save()  # Сохраняем объект, если валидация прошла успешно
        except ValidationError as e:
            return Response({"status": "error", "message": str(e)}, status=400)
        # Создание новой записи с использованием полученных данных
        # new_record = User.objects.create(name=data["name"], surname=data["surname"], patronymic=data["patronymic"], email=data["email"])
        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно создана"}, status=201)
    else:
        # Возвращаем ошибку, если запрос не методом POST
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["PUT"])
def update_user(request, id):
    if request.method == "PUT":
        # Получение данных из тела запроса
        data = request.data
        # Получение объекта Task по его идентификатору (id)
        user = get_object_or_404(User, id=id)

        # Обновление значений полей, если они переданы в запросе
        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "patronymic" in data:
            user.patronymic = data["patronymic"]
        if "email" in data:
            user.email = data["email"]

        try:
            # Создаем экземпляр модели на основе данных
            user.full_clean()  # Выполняем валидацию
            user.save()  # Сохраняем объект, если валидация прошла успешно
        except ValidationError as e:
            return Response({"status": "error", "message": str(e)}, status=400)

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно обновлена"})

    else:
        # Возвращаем ошибку, если запрос не методом PUT
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["DELETE"])
def delete_user(request, id):
    if request.method == "DELETE":
        # Получение объекта User_Task по его идентификатору (pk)
        user = get_object_or_404(User, id=id)

        # Удаление объекта из базы данных
        user.delete()

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно удалена"})
    else:
        # Возвращаем ошибку, если запрос не методом DELETE
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


# Список задач у пользователя
class UserTaskList(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Получаем id пользователя из URL запроса
        user_id = self.kwargs['user_id']
        # Фильтруем задачи по пользователю
        queryset = Task.objects.filter(id_user=user_id)
        return queryset


# Список задач
class task_list(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Добавить задачу
@api_view(["POST"])
def create_task(request):
    if request.method == "POST":
        # Получение данных из тела запроса
        data = request.data
        if request.data["id_user"] is None:
            request.data["id_user"] = 1
        user = get_object_or_404(User, id=request.data["id_user"])
        try:
            # Создаем экземпляр модели на основе данных
            new_task = Task(name=data["name"], description=data["description"], date_start=data["date_start"], date_end=data["date_end"], id_user=user, priority=data["priority"], readiness=data["readiness"])
            new_task.full_clean()  # Выполняем валидацию
            new_task.save()  # Сохраняем объект, если валидация прошла успешно
        except ValidationError as e:
            return Response({"status": "error", "message": str(e)}, status=400)
        # Создание новой записи с использованием полученных данных
        # new_record = Task.objects.create(name=data["name"], description=data["description"], date_start=data["date_start"], date_end=data["date_end"], id_user=user, priority=data["priority"], readiness=data["readiness"])
        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно создана"}, status=201)
    else:
        # Возвращаем ошибку, если запрос не методом POST
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["PUT"])
def update_task(request, id):
    if request.method == "PUT":
        # Получение данных из тела запроса
        data = request.data
        # Получение объекта Task по его идентификатору (id)
        task = get_object_or_404(Task, id=id)

        # Обновление значений полей, если они переданы в запросе
        if "name" in data:
            task.name = data["name"]
        if "description" in data:
            task.description = data["description"]
        if "date_start" in data:
            task.date_start = data["date_start"]
        if "date_end" in data:
            task.date_end = data["date_end"]
        if "priority" in data:
            task.priority = data["priority"]
        if "readiness" in data:
            task.readiness = data["readiness"]
        if "id_user" in data:
            user = get_object_or_404(User, id=request.data["id_user"])
            task.id_user = user

        try:
            # Создаем экземпляр модели на основе данных
            task.full_clean()  # Выполняем валидацию
            task.save()  # Сохраняем объект, если валидация прошла успешно
        except ValidationError as e:
            return Response({"status": "error", "message": str(e)}, status=400)

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно обновлена"})

    else:
        # Возвращаем ошибку, если запрос не методом PUT
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)


@api_view(["DELETE"])
def delete_task(request, id):
    if request.method == "DELETE":
        # Получение объекта User_Task по его идентификатору (pk)
        task = get_object_or_404(Task, id=id)

        # Удаление объекта из базы данных
        task.delete()

        # Возвращаем успешный ответ
        return Response({"status": "success", "message": "Запись успешно удалена"})
    else:
        # Возвращаем ошибку, если запрос не методом DELETE
        return Response({"status": "error", "message": "Метод не разрешен"}, status=405)

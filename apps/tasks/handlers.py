from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import models, serializers
from accounts.models import User


class OnlineTrainingTasksHandler(APIView):
    def get(self, request):
        online_training_tasks = models.OnlineTrainingTask.objects.all().order_by(
            "-created_at"
        )
        online_training_tasks_serializer = serializers.OnlineTrainingTaskSerializer(
            online_training_tasks, many=True
        )

        return Response(
            data=online_training_tasks_serializer.data, status=status.HTTP_200_OK
        )

    def post(self, request):
        name = request.data.get("name")

        """ Create the parent task object """
        task = models.OnlineTrainingTask.objects.create(name=name, is_active=True)

        """ Create task members """
        assigned_users = request.data.get("assignedUsers")
        for task_member in assigned_users:
            models.OnlineTrainingTaskMember.objects.create(
                task=task,
                user=User.objects.get(id=int(task_member["userId"])),
                tasks_per_turn=int(task_member["tasksPerTurn"]),
                number_of_assigned_tasks=0,
            ).save()

        task.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        task_id = request.query_params.get("taskId")
        task = models.OnlineTrainingTask.objects.get(id=int(task_id))
        task.delete()

        return Response(status=status.HTTP_205_RESET_CONTENT)


def user_got_turn():

    staff_member = None

    try:

        active_task = models.OnlineTrainingTask.objects.get(is_active=True)
        task_members = models.OnlineTrainingTaskMember.objects.filter(task=active_task)

        """ Check if tasks needs to be resetted """

        last_task_member = task_members.last()

        if last_task_member.number_of_assigned_tasks == last_task_member.tasks_per_turn:
            for task_member in task_members:
                task_member.number_of_assigned_tasks = 0
                task_member.save()

        for task_member in task_members:
            if task_member.tasks_per_turn != task_member.number_of_assigned_tasks:
                staff_member = task_member.user
                task_member.number_of_assigned_tasks += 1
                task_member.save()

                break
    except:
        staff_member = None

    return staff_member

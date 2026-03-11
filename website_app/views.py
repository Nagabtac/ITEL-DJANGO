from django.shortcuts import render, redirect
from .models import Student


# READ
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


# CREATE
def addStudent(request):
    if request.method == "POST":
        name = request.POST['name']
        course = request.POST['course']
        motto = request.POST['motto']

        Student.objects.create(
            name=name,
            course=course,
            motto=motto
        )
        return redirect('student_list')


# DELETE
def deleteStudent(request):
    if request.method == "POST":
        id = request.POST['id']
        student = Student.objects.get(id=id)
        student.delete()
        return redirect('student_list')


# OPEN UPDATE PAGE
def updatePage(request):
    if request.method == "POST":
        id = request.POST['id']
        student = Student.objects.get(id=id)
        return render(request, 'students/update.html', {'student': student})


# UPDATE DATA
def updateInfo(request):
    if request.method == "POST":
        id = request.POST['id']
        student = Student.objects.get(id=id)

        student.name = request.POST['newName']
        student.course = request.POST['newCourse']
        student.motto = request.POST['newMotto']
        student.save()

        return redirect('student_list')
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.shortcuts import redirect, render

from .forms import StudentLoginForm, StudentSignupForm
from .models import Allotment, Room, Student

# Student Registration
def student_signup(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            registration_id = form.cleaned_data["registration_id"]
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            cet_percentile = form.cleaned_data["cet_percentile"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(username=registration_id, password=password)
            user.first_name = name
            user.save()

            Student.objects.create(
                registration_id=registration_id,
                name=name,
                category=category,
                cet_percentile=cet_percentile,
                user=user,
            )

            messages.success(request, "Registration successful!")
            return redirect("student_login")
    else:
        form = StudentSignupForm()

    return render(request, "hostel/signup.html", {"form": form})

# Student Login
def student_login(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student = authenticate(
                username=form.cleaned_data["registration_id"],
                password=form.cleaned_data["password"],
            )
            if student is not None:
                login(request, student)
                return redirect("student_dashboard")
            else:
                messages.error(request, "Invalid login credentials. Please try again.")
    else:
        form = StudentLoginForm()

    return render(request, "hostel/login.html", {"form": form})

# Student Logout
def student_logout(request):
    logout(request)
    return redirect("student_login")

# Faculty Login Placeholder
def faculty_login(request):
    # Implement faculty login logic here
    pass

# Rector View and Automatic Allotment
@login_required
def rector_view(request):
    if request.method == 'POST' and 'automatic_allot' in request.POST:
        print("Automatic allotment process started.")

        # Step 1: Annotate students with row numbers partitioned by category and ordered by CET percentile
        students_with_rank = Student.objects.annotate(
            rank=Window(
                expression=RowNumber(),
                partition_by=[F('category')],
                order_by=F('cet_percentile').desc()
            )
        ).filter(rank__lte=2)  # Limit to top 2 students per category

        print(f"Students with rank annotated: {list(students_with_rank.values('id', 'name', 'category', 'cet_percentile', 'rank'))}")

        # Step 2: Exclude students who have already been allotted rooms
        available_students = students_with_rank.filter(allotment__isnull=True)
        print(f"Available students for allotment: {list(available_students.values('id', 'name', 'category'))}")

        # Step 3: Get available rooms (rooms that are not yet full)
        available_rooms = Room.objects.filter(current_capacity__lt=F('total_capacity')).order_by('room_number')
        print(f"Available rooms: {list(available_rooms.values('id', 'room_number', 'current_capacity', 'total_capacity'))}")

        if not available_rooms.exists():
            messages.error(request, 'No rooms are available for allotment!')
            print("No rooms available for allotment!")
            return redirect('rector_view')

        # Step 4: Allocate students to rooms (updating room capacity)
        for student in available_students:
            print(f"Processing student: {student.name} from {student.category}")

            # Check if we have any available rooms left
            room = available_rooms.first()  # Get the first available room

            if room:
                print(f"Allocating {student.name} to Room {room.room_number}. Current capacity: {room.current_capacity}")
                
                # Allot student to the room
                Allotment.objects.create(student=student, room=room)
                
                # Increase the current capacity of the room
                room.current_capacity += 1
                room.save()

                # Show success message
                messages.success(request, f'{student.name} from {student.category} category allotted to Room {room.room_number}.')

                # If room is now full, remove it from available rooms
                if room.current_capacity >= room.total_capacity:
                    print(f"Room {room.room_number} is now full. Removing from available rooms.")
                    available_rooms = available_rooms.exclude(id=room.id)

            # If no more rooms available, stop allocation
            if not available_rooms.exists():
                messages.warning(request, 'No more rooms available for allotment!')
                print("No more rooms available for allotment! Stopping allocation process.")
                break

        print("Automatic allotment process completed.")
        return redirect('rector_view')

    # Get all students (both allotted and unallotted) and their allotment status
    students = Student.objects.all()
    rooms = Room.objects.filter(current_capacity__lt=F('total_capacity'))  # Rooms that are not full

    context = {
        'students': students,
        'rooms': rooms,
    }

    return render(request, 'hostel/rector_view.html', context)

# Rector Login
def rector_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        rector = authenticate(username=username, password=password)
        if rector is not None:
            login(request, rector)
            return redirect("rector_view")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "hostel/rector_login.html")

# Rector Logout
@login_required
def rector_logout(request):
    logout(request)
    return redirect("home")  # Redirect to the home page

# Student Dashboard
@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        allotment = Allotment.objects.get(student=student)  # Get the student's allotment
    except Student.DoesNotExist:
        messages.error(request, "Student record not found. Please contact support.")
        return redirect("student_login")
    except Allotment.DoesNotExist:
        allotment = None  # No room allotted

    context = {
        "student": Student,
        "allotment": allotment,  # Include the allotment in the context
    }
    return render(request, "hostel/student_dashboard.html", context)

# Student View
def student_view(request):
    return render(request, "hostel/student_view.html")

# Home Page
def home(request):
    return render(request, "hostel/home.html")

# Allot Rooms (currently redirects to rector view)
@login_required
def allot_rooms(request):
    return redirect("rector_view")

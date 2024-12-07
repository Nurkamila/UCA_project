# School Management and Student Transfer System

## Problem statement
Traditionally, student transfer processes between schools have relied heavily on physical documentation, which has led to several issues:

1) **Document Loss:** Important student records were often misplaced or lost during the transfer process.

2) **Inefficiency for Distant Transfers:** Students 
transferring to schools located far away, sometimes requiring hours of travel, had to:
    * Visit the new school to obtain approval from the director.
    * Notify their current school.
    * Return to the new school to finalize the transfer.
    
    This process was time-consuming and inconvenient for both students and administrators.
## Solution
This project addresses the challenge of managing school personnel, students, and their academic records within a centralized system.

1) **Document Security:** All student records are stored digitally, ensuring they are never lost and can be accessed at any time by authorized personnel.

2) **Streamlined Process:** 
    * The platform allows directors to initiate and complete student transfers without physical travel or excessive paperwork.
    * Transfers can be managed entirely online, saving time and reducing manual errors.

3) **Access Management:**
    * After a transfer is initiated, access to the student profile is adjusted.
    * The original school loses access upon completion of the transfer, while the new school gains full access to the student's records.

This system significantly improves efficiency, reduces the risk of errors, and makes the transfer process convenient for all stakeholders.

The system is built with Django REST Framework (DRF), making it scalable, secure, and easy to integrate with other systems.

## Key Features of The Project

1) **Region and School Management:** Tracks schools and their respective regions with unique codes for secure identification.
2) **User Roles:** Defines user roles as teacher or director, ensuring role-based access control.
3) **Student Management:** Enables teachers to manage student profiles and academic records.
4) **Student Transfer System:** Allows directors to initiate and complete student transfers between schools while revoking access from the old school staff and granting it to the new staff.
5) **Grade Management:** Tracks student performance across different subjects, grades, and academic years.

## Models Overview
**Model ```Region```**
* Represents geographical regions where schools are located.
* Attributes:
    * ```name```: Name of the region (unique).

**Model ```School```**
* Represents schools under different regions.
* Attributes:
    * ```name```: School name
    * ```region```: Foreign key to the ```Region``` model.
    * ```code```: A unique identifier generated automatically for secure validation.

* Methods:
    * ```get_director```: Fetches the email of the current director for the school.

**Model ```User```**
* Custom user model extending.
* Attributes:
    * ```email```: Used as the unique identifier for authentication.
    * ```role```: Role of the user (teacher or director).
    * ```region``` and ```school```: Links users to specific schools and regions.

**Model ```StudentProfile```**
* Represents student information.
* Attributes:
    * ```first_name```, ```last_name```, ```middle_name```: Personal details.
    * ```photo```: Uploaded photo of the student.
    * ```teacher```: Assigned teacher.
    * ```school``` and ```region```: Links to the student's current school and region.
    * ```pending_transfer_school```: Tracks transfer requests to a new school.

**Model ```Subject```**
* Represents subjects offered in schools.
* Attributes
    * ```subject_name```: Name of the subject (unique).

**Model ```Grade```**
* Tracks student performance in different subjects and school years.
* Attributes:
    * ```student_profile```: Foreign key linking the grade to a specific student.
    * ```subject```: Foreign key linking to the ```Subject``` model.
    * ``` quarter_1, quarter_2, quarter_3, quarter_4 ```: Grades for each quarter.
    * ```year_average```: Automatically calculated average for the year.

## Serializers Overview
```RegistrationSerializer```
* Used for user registration.
* Validates that the selected school belongs to the given region and checks the school's unique code.

```UserSerializer```
* Serializes basic user information (first name, last name, middle name).

```StudentProfileSerializer```
* Serializes student profile data, including personal details and grades.
* Overrides the ```create``` method to automatically link the student to the teacher, school, and region of the logged-in user.

```GradeSerializer```
* Serializes grade data.
* Calculates the ```year_average``` based on non-empty quarter grades during updates.

```StudentTransferSerializer```
* Serializes the ```new_school``` attribute for transfer requests.

## Views Overview

```RegistrationView```
* Allows users to register as teachers by providing valid school and region details.

```ListTeachers```
* Lists all teachers in the current director's school.
* Restricted to directors only.

```StudentProfileViewSet```
* Manages student profiles.
* Actions:
    * ```assign_teacher```: Allows a director to assign a teacher to a student.
    * Handles searching by student name.

```GradeViewSet```
* Manages student grades.
* Ensures teachers can only modify grades for their assigned students.

```StudentTransferViewSet```
* Handles student transfer functionality.
* Actions:
    * ```transfer_student```: Initiates a student transfer to a new school.
    * ```complete_transfer```: Completes the transfer and updates the student's school and region.

## Technologies and Libraries Used
* Django web framework.
* Django REST Framework (DRF) to build web APIs in Django.
* Django REST Framework Simple Json Web Token (JWT) authentication.
* drf-yasg for creating interactive API documentation (Swagger).
* django-filter for searching and filtering student profiles.
* PostgreSQL Database

## Installation and Usage

**Prerequisites:**
* Install Python 3.8 or higher.
* Install PostgreSQL
* Install pip3

**Clone the Repository:**
```bash
git clone https://github.com/Nurkamila/UCA_project.git
cd UCA_project
```

**Install Dependencies:**
```bash
pip install -r req.txt
```

**Create a .env File:**
* In the downloded folder create a file named .env and include the following environment variables for the database connection:

```
DB_NAME=<name_of_your_database>
DB_USER=<postgres_username>
DB_PASSWORD=<postgres_password>
```

**Run Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Start the Server:**
```bash
python manage.py runserver
```

**API Endpoints:**
```
Here is a link to swagger documentation where you can find all endpoints

http://127.0.0.1:8000/docs/
```
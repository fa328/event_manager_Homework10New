# Homework 10

## Close issue 
1. update password length constraint #1
2. Add a minimum and maximum length constraint #3
3. Update UserUpdate class to None #4
4. fix test_create_user_access_denied error #5 
5. fix test_update_user_email_access_denied error #6

## Dockerhub Image
![image](https://github.com/user-attachments/assets/0cc11f3c-fbcc-4f7e-a65f-17adb0794ded)
![image](https://github.com/user-attachments/assets/c1e8af6c-be6d-4d78-baef-709cbb0ee2a2)


## Reflection
This assignment was incredibly interesting and provided me with valuable experience in debugging and learning through trial and error. I believe the project addresses a real-world problem, and it offers a great opportunity to understand what to expect in similar situations while also improving students' skills. By working through this project, students are not only encouraged to fix errors in the code but also to learn from the mistakes they make along the way. I found the debugging process particularly challenging because, at times, I wasn't sure if I was truly fixing the error or unintentionally creating new ones. Despite this, the experience helped me develop a deeper understanding of problem-solving and the iterative nature of debugging.

As I reviewed the code, I noticed that the nickname field was already being validated using a regular expression pattern. However, there was no maximum length set for the password. To address this, I ensured that the nickname field had a reasonable length constraint, limiting it to 3 to 50 characters. While reviewing the user schema, I also focused on enforcing best practices for secure passwords. To improve security, I added a validator to the UserCreate model that checks the password for several criteria: a minimum length, at least one uppercase letter, at least one lowercase letter, at least one digit, and at least one special character. By implementing these changes, I aimed to enhance both the user experience and the security of the application.



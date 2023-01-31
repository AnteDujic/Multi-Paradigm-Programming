# MULTI PARADIGM PROGRAMMING | 2022/2023
### AUTHOR: ANTE DUJIC
<hr style="border:2px solid gray"> </hr>

This repository contains the project done for the Multi Paradigm Programming course on ATU, Ireland. The aim of the project is to design a Shop applications in Python and C, using Object Oriented and Procedural paradigms and write a report which compares the solutions achieved using the mentioned paradigms. There are three folders each containing one application:
1. :file_folder: c
2. :file_folder: python
3. :file_folder: python_OOP

The requirements for the applications are as follows:
- Shop CSV holds the inital cash value for the shop
- Customer orders are read from CSV
    - File includes all the products and the quantity
    - File includes customer name and the budget
- Shop processes the customer order
    - Shop cash updates
    - There are different customers
        - Customer whose order can be proccessed as planned
        - Customer who doesn't have enough money for the purchase
        - Customer who wants to buy more items then available on stock
- Shop has a live shopping option
    - User enters its name and budget
    - User enters product name and quantity
    - Complete the transaction
- User experience in all applications HAS to be identical


### [REPORT](https://github.com/AnteDujic/Multi-Paradigm-Programming/blob/main/report.pdf) CONCLUSION

While Object-oriented approach might be harder to grasp at the start, I found it to be more suitable to create a Shop application. The main reason being the easier translation of the real-world environment into the code. This made accessing certain variables more logical. Apart of that, I found both approaches to be very similar in terms of code navigation and maintenance. This is likely due to the applications size, which is not too big. As the size of the application would become bigger, I think using Object oriented approach would prove to be a better choice. Both approaches allowed for code reusability with this being even further extended using Object Oriented paradigm, due to the ability of inheritance. Using C language proved to be challenging at times, but this is because of the way I am used to think, using mainly Python prior to this project. This, however is not connected to the paradigm but the fact that C is a different programming language.

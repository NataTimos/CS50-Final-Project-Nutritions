# Nutritions

## Final Project from Harvard's Introduction to Computer Science CS50 hosted on eDX

*The climax of this course is its final project. I chose to create a web-based food caculator.*
My verifide ceftificate: https://courses.edx.org/certificates/33c624beada54049b8ae8d50d03ea2f3

#### [Nutritions CS50 final project Demo Video](https://youtu.be/Y2jzpcygD6Y)

Image is link to the video too :)
[![Nutritions CS50 final project](https://github.com/NataTimos/Nutritions/blob/main/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202021-02-10%20%D0%B2%2015.20.51.png)](http://www.youtube.com/watch?v=Y2jzpcygD6Y)

### Description
  >Nutritions is a web app I created that shaws all nutritions (46 items in total) from food products someone's ate.

  >Without registration, the user can see the composition of a separate product.

  >To add or to remove product to the food diary, view the total amount of nutrients in the food diary, the user must register.


#### product database was taken from [USDA National Nutrient Database](https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/methods-and-application-of-food-composition-laboratory/mafcl-site-pages/sr11-sr28/)

> The USDA National Nutrient Database for Standard Reference is a database produced by the United States Department of Agriculture that provides the nutritional content of many generic and proprietary-branded foods.

> Released in August 2015 and revised in May 2016, the current release, Standard Reference 28 (SR28), contains "data on 8,800 food items and up to 150 food components".

> New releases occur about once per year. The database may be searched online, queried through a representational state transfer API, or downloaded.

#### Technology Used
* python
* flask
* sqlite
* html
* css
* bootstrap
* databases

#### Features
* Register:
  * register new user to be able to use food claculator full features.
* Login:
  * login to existing user account.
* Logout:
  * log out from account
* Homepage:
  - the form prompts user to enter a keyword for the product he/she are looking for,
  -  the form on the next page offers to choose one of the list of products that start with a keyword.
  - After submitting the user will see a table with the detailed composition of the product.
* Add Food:
  * after registration, the user can add the product and its quantity to the diary.
* Delete Food:
  * after registration, the user can delete the product to the diary.
* Food Diary:
  * after registration, the user can view the food diary with:
  * the table of added products and their quantity,
  * table of all nutrients in added products.

 #### Files
 * application.py - main file with code that controls page behavior
 * nutrotions.db - database with three tables:
   * 1.table of nitriets in food
   * 2.user table
   * 3.the history table of adding and removing products
 * index.html - homepage with form asking for keyword for food product
 * register.html - registration form
 * login.html - login form

# Raw Combined Transcript

## Chapter 1: Overview of Common Data Types

### Welcome!

1. Welcome!
00:00 - 00:27
Welcome to PostgreSQL Functions for Manipulating Data! My name is Brian Piccolo and I am a Sr. Director of Digital Strategy. I will be your instructor for this course. You've learned some SQL fundamentals in your previous coursework. Now we are going to continue to expand your SQL knowledge by teaching you how to use built-in functions and operators to extend the capabilities of your PostgreSQL database.

2. The Sakila Database
00:27 - 00:46
You'll be using the Sakila Database which is a well known example database that models a fictional DVD rental store. The database is highly normalized which allows for great sample queries and provides a great representation of PostgreSQL data types and custom functions.

3. Topics
00:46 - 01:22
Before we get started let's review the topics that will be covered in this course. First in this chapter, you'll learn about some common data types and their properties and characteristics. Next you'll dive into some built-in functions and operators and learn how to use them to manipulate date and time data. You'll then explore some frequently used functions for parsing and manipulating text data types. And finally you'll get an introduction into full-text search using PostgreSQL extensions. Let's get started.

4. Common data types
01:22 - 01:59
PostgreSQL has a robust set of native data types. Some of the most common include: Text data types like CHAR, VARCHAR and TEXT Numeric data types like INT and DECIMAL Date and time types such as DATE, TIME, TIMESTAMP and INTERVAL. And finally ARRAYs. It's important to have an understanding of the properties and characteristics of the various data types anytime you are working with a relational database like PostgreSQL.

5. Text data types
01:59 - 02:32
Text data types like CHAR and VARCHAR allow for a fixed or varying number of characters and string data. Think about categorical data like the title column from the film table. TEXT data types typically represent character and string data but can be an unlimited length. For example, the text from the description column in the film table. We'll explore how to extract, create substrings and manipulate text data types later on in this course.

6. Numeric data types
02:32 - 02:52
Numeric data types like INT and DECIMAL allow you to store integers like payment_id and floating point numbers with varying precisions like amount from the payment table. We'll learn more about PostgreSQL date and time and array data types later in this chapter.

7. Determining data types from existing tables
02:52 - 03:18
When you are working with existing databases, there will be times when you need to determine the data types of columns that you'll be working with. For example, if we look at the results from a simple SELECT query on the film table, you might hypothesize that all the columns in this query have a text data type. But, would you be right? Let's take a closer look.

8. Determining data types from existing tables
03:18 - 04:07
PostgreSQL stores information about all database objects in a system database called INFORMATION_SCHEMA. By querying certain tables in this database, you can determine information about the database including data types of columns. The following query will return the column_name and the data type for the columns we looked at in the previous slide. When you execute this query, you will get a result that looks like the following. If we look closely at these results we see that the title and description columns are indeed text data types, specifically VARCHAR and TEXT. But we see that special_features is actually an ARRAY. You'll learn more about ARRAYs later in this chapter.

9. Let's practice!
04:07 - 04:15
Now it's your turn. Let's take a closer look at the customer table of our DVD Rentals database.

### Date and time data types

1. Date and time data types
00:00 - 00:19
Next up we will learn about some common date and time data types. Understanding how to work with these data types is crucial for preparing and extracting data for machine learning and data science. In this lesson, you will learn about the precision and features of timestamps, intervals and date and time types.

2. TIMESTAMP data types
00:19 - 01:11
You'll find that most of the date and time data you'll be working with in SQL will have a TIMESTAMP data type. TIMESTAMPs contain both a date value and a time value with microsecond precision. These data types are very common because they can be used to record an exact point in time like when a payment was made or a record was last updated. TIMESTAMPs in PostgreSQL use the ISO 8601 format which is a four digit year followed by a two digit month and day separated by dashes. If you look in the payment table of the Sakila database, you'll see what this format looks like. Notice that the values contain both a date and a time value with seconds precision where the example above was at the microsecond precision.

3. DATE and TIME data types
01:11 - 01:50
Next, you'll look at DATE and TIME types. When you only need to store a part of the TIMESTAMP in your database, the DATE and TIME types may be better options. DATE and TIME types are essentially the date and time values of the TIMESTAMP. As you see in this example, DATE types contain a date value with no time of day while TIME types contain the time of day but without, you guessed it, a date. If we look at the create_date from the customer table of our DVD rental database you'll see an example of a DATE type.

4. INTERVAL data types
01:50 - 02:22
Finally INTERVAL types store date and time data as a period of time in years, months, days, hours, seconds, etc. For example, 4 days. INTERVALs are useful when you want to do arithmetic on date and time columns. Here you'll see a query where we calculate an expected return date based on a 3 day rental duration by adding an INTERVAL of 3 days to the rental_date column from the rental table in our DVD database.

5. Looking at date and time types
02:22 - 03:02
We can use the same technique that we learned in the previous lesson to determine information about a column with a date and time type by querying the INFORMATION_SCHEMA system database. If we look at the rental_date column of the rental table you'll see that this is a TIMESTAMP. However, you'll also notice the "without time zone" reference. PostgreSQL provides you with the ability to store TIMESTAMP and TIME data types with or without a timezone. While this comes in handy in certain situations, most of the time you'll work with TIMESTAMP values without a timezone which is the default behavior.

6. Let's practice!
03:02 - 03:10
Now it's your turn. Let's take a closer look at date and time data types in the exercises.

### Working with ARRAYs

1. Working with ARRAYs
00:00 - 00:19
Welcome back! Now you will get a bit more advanced as we begin to explore ARRAY data types. Arrays in PostgreSQL are very similar to arrays in most programming languages. You can create multi-dimensional arrays of varying lengths for any native data type in PostgreSQL.

2. Before we get started
00:19 - 01:12
Before we get started, we want to quickly touch on some concepts that you'll be using in this lesson. Most data science requires getting data out of a database using SQL queries with SELECT statements. But before you are able to extract data, someone needs to create the database, add at least one table with at least one column and then insert some records. The CREATE TABLE command as you see in this example, will create an empty table called my_first_table with the columns first_column and second_column defined as text and integer data types. The INSERT statement example here will add one record into my_first table with 'text value' as the value for the first column and 12 as the value for the second column.

3. ARRAY a special type
01:12 - 01:55
Now that you have learned some basics about the CREATE TABLE command and INSERT statements, let's see how you can use these skills to create and manipulate ARRAY types. To create an ARRAY type, you simply need to add "square brackets" to the end of the data type that you want to make an array. Let's create a simple table with two array columns to illustrate how this is done. This table has an email column which will be a nested array of text data to store the email type and the address for a given student_id. The test_scores column will contain an array of integer values representing the numeric test score.

4. INSERT statements with ARRAYS
01:55 - 02:13
Once the table is created we can use the INSERT STATEMENT to add a couple of records to the table. Notice how arrays are represented in the SQL with curly brackets and single quotations for email and comma separated list of whole numbers for test_scores.

5. Accessing ARRAYs
02:13 - 02:42
Now that we have data in our table, let's see how you access array data in a SELECT statement. Accessing arrays in PostgreSQL is very similar to accessing arrays in other programming languages. For email, you can get the first element of the first array by using the array notation you see here with index values of 1. Note that PostgreSQL array indexes start with one and not zero.

6. Searching ARRAYs
02:42 - 03:05
The same notation used to access ARRAYs in the SELECT statement, can also be used in the WHERE clause as a filter. Here we look for records that have 'work' as a value in the first index of the email ARRAY. Using standard syntax for non-array columns like WHERE email='work' would generate an error.

7. ARRAY functions and operators
03:05 - 03:43
The ANY function allows you to search an array for a value and return a record if it finds a match. In this example, we want to query all records where the email address contains 'other' in any value of the array. Notice the null values for type and address. Remember the second record we created earlier in this lesson only had one email address of type work. This means that when we access the second index value for this record by using the number 2 in the first set of square brackets, it would be null because it doesn't exist.

8. ARRAY functions and operators
03:43 - 03:57
An alternative to the ANY function is the contains operator. The syntax for this operator is a bit more complex but will return the same results as the ANY function as shown in the output below.

9. Let's practice!
03:57 - 04:03
Now it's your turn to get some practice working with arrays in the exercises

## Chapter 2: Working with DATE/TIME Functions and Operators

### Overview of basic arithmetic operators

1. Overview of basic arithmetic operators
00:00 - 00:11
Now that you have learned the fundamentals of PostgreSQL data types, it's time to learn how to manipulate these data types to assist with your data cleansing and transformation tasks.

2. Topics
00:11 - 00:54
In this chapter, you'll dive into some built-in date and time functions and operators and learn how to use them to manipulate date and time data. First in this video, you'll learn how to add and subtract date and time values and understand the expected behavior of each operation. Next, you'll learn how to use these functions to retrieve the current date and time. You'll then look at how to use the AGE function to calculate the difference between two timestamps. And finally you'll learn how to use the EXTRACT, DATE_PART, and DATE_TRUNC functions to manipulate timestamps to retrieve subfields of date and time values. Let's get started.

3. Adding and subtracting date / time data
00:54 - 01:19
Performing basic arithmetic operations on date and time data types will become a useful skill in practice but it's important to understand how the return values for these operations vary depending on the type of date and time data types you are working with. For example, when you subtract date values, the result that is returned is an integer data type.

4. Adding and subtracting date / time data
01:19 - 01:38
You can also add integer values to date data types. In this example, we are adding the whole number three to a date value and getting a result that is three days greater than the original date. When adding integers to date values, the implied precision is days.

5. Adding and subtracting date / time data
01:38 - 01:50
However, when we perform the same operation on timestamp data types as you see in this example, we get an INTERVAL as the result.

6. Calculating time periods with AGE
01:50 - 02:11
The AGE function allows us to calculate the difference between two timestamps. The AGE function takes two timestamp arguments and subtracts the first argument from the second and returns an INTERVAL as a result. You'll notice in this example that the result is identical to what we calculated on the previous slide.

7. DVDs, really??
02:11 - 02:41
I'm sure that at this point in the course you've questioned why we are using a fictional DVD rental store as our sample dataset. And it would be a valid question. As we talked about earlier in the course, the Sakila database is a widely used sample dataset for working with and learning about relational databases. In fact, it's been more than 13 years since the data in this database was created and the `AGE()` function is a great way to highlight this.

8. Date / time arithmetic using INTERVALs
02:41 - 03:05
Learning how to use INTERVALs for your date and time calculations is a very useful skill to develop with real world applications. Using an INTERVAL is a great technique when you need to complete relative date and time calculations. If you recall in the first chapter, we calculated the expected_return date by adding an INTERVAL of 3 days to the rental_date column.

9. Date / time arithmetic using INTERVALs
03:05 - 03:38
You can also perform multiplication and division on date and time data types using intervals which is another useful tool when you have relative date and time data. For example, let's say we wanted to add 21 days to a date value. As you recall from earlier in this video, when you are working with a date data type, you can just add an integer to the date. However, what if you need to perform this calculation with a timestamp? This is where INTERVALs come in handy as you see in this example.

10. Let's practice!
03:38 - 03:47
Great work! Now let's practice performing basic arithmetic operations on date and time values in the exercises.

### Functions for retrieving current date/time

1. Functions for retrieving current date/time
00:00 - 00:09
Great work! Now we are going to learn how to retrieve and use the current date and time value in your queries at varying levels of precision.

2. Retrieving the current timestamp
00:09 - 00:35
As you expand your SQL expertise, one of the most common techniques you'll use is to retrieve the current date and time value in your query. PostgreSQL provides several functions for doing this and we'll explore a few in this video beginning with the NOW() function. NOW() allows you to retrieve a timestamp value for the current date and time at the microsecond precision with time zone.

3. Retrieving the current timestamp
00:35 - 00:46
Many times you will want to retrieve the current timestamp without the timezone. You can do this by explicitly casting it as seen in this example.

4. Retrieving the current timestamp
00:46 - 01:28
Casting allows you to convert one data type to another such that columns stored in your database can be retrieved and output as a different type. There are a couple of ways you can cast data in your queries. We saw how to cast the timestamp returned by the NOW() function on the previous slide by adding two colons followed by the new type name. This syntax which uses the double colon operator is specific to PostgreSQL and non-conforming to the SQL standard. You can also use the CAST() function to achieve the same result by specifying the column name or in this case the NOW() function followed by the type name.

5. Retrieving the current timestamp
01:28 - 01:47
PostgreSQL provides alternative methods for retrieving the current date and time values. The CURRENT_TIMESTAMP function returns the same result of the NOW() function as you see in this example and either approach can be used pretty much interchangeably in your queries.

6. Retrieving the current timestamp
01:47 - 02:05
One difference between CURRENT_TIMESTAMP and NOW() is that with CURRENT_TIMESTAMP you can specify a precision parameter as you see in the example which will cause the result to have the seconds rounded to the number of fractional digits specified.

7. Current date and time
02:05 - 02:26
Sometimes you want to get the current date or time but don't require the precision of a timestamp. In these instances you can use the CURRENT_DATE and/or CURRENT_TIME functions to achieve this. In this example, the CURRENT_DATE function will return a date value without the time.

8. Current date and time
02:26 - 02:36
Additionally, you can use the CURRENT_TIME function to get the time value with timezone without the date value as seen in this example.

9. Let's practice!
02:36 - 02:49
In the exercises, you'll get some experience on how to retrieve the current timestamp and use what you learned in the previous video to do some arithmetic operations with these results.

### Extracting and transforming date / time data

1. Extracting and transforming date / time data
00:00 - 00:19
In a previous video, you learned about the AGE function and how to use it to calculate the difference between two timestamps. Next we'll look at some additional built-in functions that will help us transform timestamp and interval data types and create new fields that will help us prepare data for analysis.

2. Extracting and transforming date and time data
00:19 - 01:02
Let's start by taking a look at how we can use the EXTRACT, DATE_PART and DATE_TRUNC functions to manipulate timestamp data and create new columns by extracting sub-fields from existing date and time values. This type of data manipulation is useful when the precision of a timestamp is not useful for analysis and you want to use date parts like year or month in your queries but the underlying data only contains a standard timestamp value. You may also not care about certain precision like time of day in some analyses and truncating timestamps may be necessary.

3. Extracting and transforming date / time data
01:02 - 01:51
This is where the EXTRACT and DATE_PART functions come in very handy. To use these functions in your queries you will need to pass two parameters. The field identifier and the source. The field parameter is an identifier (or string if you are using DATE_PART) that indicates what sub-field that you want to extract from the source. The various field identifiers include year, month, quarter, day of week, etc. The source parameter needs to be a valid timestamp, time, or interval data type. Both EXTRACT and DATE_PART will produce identical results and can be used interchangeably with only slight variations in how you pass in the field and source parameters. Now, let's get into some examples and see this in action.

4. Extracting sub-fields from timestamp data
01:51 - 02:22
In our DVD Rentals database, every customer rental has a corresponding record in the payment table and each transaction is recorded with a timestamp in the payment_date column as the snippet below highlights. This level of detail is certainly necessary for an e-commerce application, but there will no doubt be times when you will want to be able to aggregate this data to use for training a model, reporting and/or trend analysis.

5. Extracting sub-fields from timestamp data
02:22 - 03:03
For example, you may want to identify the highest revenue by quarter. To do this we'll want to aggregate the amount column from the payment table and use the EXTRACT function to extract the quarter and year sub-fields from the payment_date column. Here you'll see that we also introduce a technique with the GROUP BY clause that allows us to specify the fields in the SELECT clause using a numeric reference which comes in handy when using functions to derive new columns. And you see the results of the query here which aggregates the amount column grouped by quarter and year.

6. Truncating timestamps using DATE_TRUNC()
03:03 - 03:51
The DATE_TRUNC() function will truncate timestamp or interval data types to return a timestamp or interval at a specified precision. The precision values are a subset of the field identifiers that can be used with the EXTRACT() and DATE_PART() functions. For example, to truncate a date by year we pass the year identifier as the first parameter of the DATE_TRUNC function, as you see here and get the following result. Or we can truncate the same timestamp using month as the parameter and get this result. Unlike these functions, DATE_TRUNC() will return an interval or timestamp rather than a numeric value.

7. Let's practice!
03:51 - 03:58
Let's put these new skills to use in the exercises!

## Chapter 3: Parsing and Manipulating Text

### Reformatting string and character data

1. Reformatting string and character data
00:00 - 00:14
Great job! Understanding how to manipulate and transform date and time data types will be something you use often in your data science work. Next we are going to learn how to manipulate and transform string and character data.

2. Topics
00:14 - 00:41
In this chapter we will begin by learning about functions and operators that allow us to reformat string and character data. Next you'll explore functions that allow you to parse string and character data. You will then learn how to calculate the length of a string or determine the position of a character within a string. And finally you'll learn how to truncate and pad string data. Let's get started.

3. The string concatenation operator
00:41 - 01:13
First we will look at one of the most common and frequently used techniques when working with string data. String concatenation allows you to merge two or more strings together to form a single combined string. In this example, you see how we can combine two separate columns from the customer table, first_name and last_name, to create a new column called full_name. This is one of many real world scenarios that will require you to concatenate strings.

4. String concatenation with functions
01:13 - 01:46
Additionally, PostgreSQL also has a built-in function for string concatenation. The CONCAT() function accepts one or more parameters and returns the concatenated string as the result. Each parameter can be a column from a database or a literal value separate by a comma. In this example, we see how we can perform the same concatenation operation using this function rather than the || operator from the previous slide and it will produce an identical result.

5. String concatenation with a non-string input
01:46 - 02:08
PostgreSQL also allows you to concatenate both string and non-string data. As we see in this example, we prepend the customer_id column to the first_name and last_name columns. Non-string data can be used in concatenation with both the || operator as well as the CONCAT() function.

6. Changing the case of string
02:08 - 02:38
There will also be times when you want to reformat string data to uppercase, lowercase or title case. This comes in handy when you want to standardize a field in your dataset for manipulation. The UPPER function allows you to reformat a string so you change every character to its uppercase equivalent. UPPER accepts a string as a parameter and returns that string in all uppercase. Transforming string data will be useful when normalizing and cleansing datasets.

7. Changing the case of string
02:38 - 02:49
The LOWER function is analogous to UPPER but converts the string to lowercase instead. Here you see an example with the title column from the film table.

8. Changing the case of string
02:49 - 02:57
Similarly, the INITCAP function will convert a string to title case.

9. Replacing characters in a string
02:57 - 03:13
The REPLACE function will find a substring in a string and replace it with a different substring. Look at the results of the following query. You'll notice that the phrase "A Astounding" that is present in the first few rows is grammatically incorrect.

10. Replacing characters in a string
03:13 - 03:42
So let's say we want to fix this and replace all occurrences of 'A Astounding' with the proper 'An Astounding' text. We can use the REPLACE function to accomplish this task. The function takes three parameters. The first is the source string that you want to manipulate, the second is the substring you want to find in the source string and the last parameter is the replacement string.

11. Manipulating string data with REVERSE
03:42 - 03:56
The REVERSE function does just what you think it does...it accepts a string as its only parameter and returns the same string in reverse order as you see when we use the function to reverse the title column of the film table.

12. Let's practice!
03:56 - 04:01
Now it's your turn! Let's get some practice using these functions.

### Parsing string and character data

1. Parsing string and character data
00:00 - 00:13
Next up we will learn about string functions in PostgreSQL that allow us to parse and manipulate text data. We will also learn how to combine and nest functions to provide additional capabilities.

2. Determining the length of a string
00:13 - 00:39
First, let's look at the CHAR_LENGTH function. The CHAR_LENGTH function can be used to determine the number of characters in a string. CHAR_LENGTH accepts a string as an input and returns the number of characters in the string as an integer for the output. In this example, we see the CHAR_LENGTH function used on the title column of the film table in the DVD Rental database.

3. Determining the length of a string
00:39 - 00:52
LENGTH is analogous to CHAR_LENGTH, accepts the same parameter and returns the same result as you can see in this example. These two functions can be used interchangeably depending on your preference.

4. Finding the position of a character in a string
00:52 - 01:08
The POSITION function returns an integer which represents the number of characters from left to right before the search string is located. Looking at the customer table we can find the position of the at sign in the email column.

5. Finding the position of a character in a string
01:08 - 01:17
STRPOS is analogous to POSITION with a slightly different syntax as you see in this example.

6. Parsing string data
01:17 - 01:36
Now let's look at some functions that will help you parse strings into substrings. The LEFT function allows you to extract the first "n" characters of a string. In this example, we are going to extract the first fifty characters of the description column from the film table in our DVD Rental database.

7. Parsing string data
01:36 - 01:46
The RIGHT function is very similar to LEFT but as you might expect it extracts the last "n" characters of a string.

8. Extracting substrings of character data
01:46 - 02:21
SUBSTRING allows us to do pretty much exactly what its name implies - extract a substring from text data. The substring functions takes 3 parameters. The first is the source string or column, in this example the description column from the film table. This is followed by an integer representing the starting position of the source string or in this case the number 10. Finally, we include another integer to specify the length of the substring that we want to extract. In this case, the number 50.

9. Extracting substrings of character data
02:21 - 03:02
SUBSTRING can be combined with other functions to provide additional capabilities. In this example, we can extract the text from the left side of the at sign in an email address using a slightly different set of parameters in the SUBSTRING function. The first parameter remains the same, but the second parameter is replaced with the FROM keyword followed by an integer representing the starting position and the third parameter includes the FOR keyword followed by an integer representing the ending position. In this example we use the POSITION function as the second parameter in the SUBSTRING function.

10. Extracting substrings of character data
03:02 - 03:38
Now we can use a different technique if we want to extract the characters to the right of the at sign in the email column. In this example, we use the POSITION function as the second parameter of SUBSTRING to determine the starting position in the string and the CHAR_LENGTH to determine the last position which is a nice trick for determining the last position of a string. The POSITION function will return the integer value of the position of the at sign in the string. To exclude the at sign from the result, we need to add one to the starting position.

11. Extracting substrings of character data
03:38 - 03:51
SUBSTR is analogous to SUBSTRING but only allows for the parameters to be separated by commas and does not allow for the alternative syntax with the FROM and FOR keywords.

12. Let's practice!
03:51 - 03:57
Now it's your turn! Let's practice using these functions in the exercises.

### Truncating and padding string data

1. Truncating and padding string data
00:00 - 00:06
Next, we are going to take a look at how to truncate and replace or overwrite characters in a string.

2. Removing whitespace from strings
00:06 - 00:48
The first function that we'll look at is the TRIM function. The TRIM function will remove characters from either the start or end of the string or both and accepts three parameters. The first parameter is optional and specifies whether you want to remove characters from the beginning or end of a string or both. If this parameter is omitted, the default value is both. The second parameter which is also optional specifies the characters to be removed from the string. If this parameter is omitted, the default value is a blank space. And finally the third parameter is the string that you wish to trim.

3. Removing whitespace from strings
00:48 - 01:03
Most of the time you'll use this function without the first two parameters and just pass a string as a single parameter. This default behavior will remove all whitespace from the beginning and end of the string as you see in this example.

4. Removing whitespace from strings
01:03 - 01:28
The LTRIM and RTRIM functions are analogous to TRIM but only remove characters from either the beginning OR the end of the string, not both. Much like TRIM, you'll use these functions with their default behavior to truncate whitespace. In this example, we see that LTRIM removes only the spaces at the beginning of the word padded but leaves the spaces at the end of the string.

5. Removing whitespace from strings
01:28 - 01:34
And you'll see the opposite result from RTRIM in this example.

6. Padding strings with character data
01:34 - 01:57
The function LPAD appends a character or string to another string by a specified number of characters. This is useful when you need a field to be the same length and want to pad the string with a certain character like a space or a tab. In this example, we are padding the word 'padded' with the hash character so that the string returned has a character length equal to ten.

7. Padding strings with whitespace
01:57 - 02:17
If you omit the third parameter in the LPAD function as you see in this example, the string will be padded with a space character by default. And when the length parameter is less than the original length of the string as you see here, the result returned will be truncated.

8. Padding strings with whitespace
02:17 - 02:24
The RPAD function is analogous to LPAD but will pad the string with characters to the right.

9. Let's practice!
02:24 - 02:29
Alright, now it's time to practice these functions with the exercises.

## Chapter 4: Full-text Search and PostgreSQL Extensions

### Introduction to full-text search

1. Introduction to full-text search
00:00 - 00:12
Great job! The last three chapters have explored many of the built-in functions available to you in PostgreSQL that will become invaluable skills for transforming and manipulating data using SQL.

2. Topics
00:12 - 00:48
In this chapter, we are going to get a bit more advanced and explore some of the features of PostgreSQL that allow you to extend its capabilities using custom code. In this chapter we'll explore: An introduction into the full text search capabilities of PostgreSQL that allow you to improve the manner by which you search text columns in your database. An overview of how to extend the features and capabilities of PostgreSQL using extensions. And finally we'll explore how to improve full text search with extensions and some advanced capabilities that you get when you combine the two.

3. The LIKE operator
00:48 - 01:30
If you remember back in the prerequisite material, the LIKE operator can be used in a WHERE clause to search for a pattern in a column. To accomplish this, you use something called a wildcard as a placeholder for some other values. There are two wildcards you can use with LIKE. The first is the underscore sign which matches exactly one character. The second is the percent sign which will match zero or more characters of variable length. In this example we use the percent wildcard to match any title from the film table that starts with the word ELF followed by zero or more characters.

4. The LIKE operator
01:30 - 01:48
Changing the position of the percent wildcard in our query produces a very different result. In this example, we use the percent sign wildcard to match a string that begins with one or more characters followed by the string ELF.

5. The LIKE operator
01:48 - 02:18
LIKE is a great tool to use when searching for specific characters in a string. Sometimes when you are preforming a text search, you will want to match variations of the characters you are searching. For example, using LIKE to search the title column for any string that contains the word elf in all lowercase will return zero results. This may be counterintuitive to what you would expect because the LIKE operator matches the exact characters in the query and is case sensitive.

6. LIKE versus full-text search
02:18 - 02:43
However, look at this query which performs a full text search by using the functions to_tsvector and to_tsquery and the match operator to search the title column. Because full text search accounts for variations of the search string and is case insensitive you will notice that you get the expected results.

7. What is full-text search?
02:43 - 03:01
So what is full-text search. Full text search provides a means for performing natural language queries of text data by using stemming, fuzzy string matching to handle spelling mistakes and a mechanism to rank results by similarity to the search string.

8. Full-text search syntax explained
03:01 - 03:43
Full text search can get complex but even a basic full text search query can be a very powerful tool. The example you see here is a basic technique for querying a document, in this case the column title, to match the characters elf. The WHERE clause of the query uses the match operator to compare the values returned by two built-in functions to perform the search, to_tsvector and to_tsquery. These functions convert text and string data to a tsvector data type which is a sorted list of words that have been normalized into variants of the same word. These variants are called `lexemes`.

9. Let's practice!
03:43 - 03:51
Alright, let's get reacquainted with the LIKE operator and compare it to basic full text search results.

### Extending PostgreSQL

1. Extending PostgreSQL
00:00 - 00:19
The previous chapters in this course have explored many of the built-in functions of PostgreSQL which provide you with powerful tools for manipulating data using SQL. PostgreSQL also provides you with the ability to create your own custom data types, functions and operators to extend the functionality of your database.

2. User-defined data types
00:19 - 01:01
Let's take a look at custom or user-defined data types. A user-defined data type is created using the CREATE TYPE command which registers the type in a system table and makes it available to be used anywhere PostgreSQL expects a type name. Enumerated data types or enums allow you to define a custom list of values that are never going to change, like the days of the week. As you can see in this example, a new data type called dayofweek is defined as an ENUM using the CREATE TYPE command with a comma separated list of the days of the week.

3. Getting information about user-defined data types
01:01 - 01:34
Once your custom data type has been created, you can query the system table called pg_type to get information about all data types available in your database both user-defined and built-in. In this query you can get the name of the data type using the typname column and the category of the data type using the typcategory column. The results of the query return dayofweek for the name of the data type that we just created and E for the category where E represents an ENUM type.

4. Getting information about user-defined data types
01:34 - 02:21
You can also use the INFORMATION_SCHEMA system database, as we learned about earlier in this course, to get information about user-defined data types. If we query INFORMATION_SCHEMA.COLUMNS and have a look at the columns in the film table specifically you'll notice that the column_name rating is a USER-DEFINED data_type with a udt_name of mpaa_rating. The udt_name column for a user_defined data type contains the value of the name provided when creating the data type using the CREATE TYPE command. You may sometimes find it necessary to learn about the characteristics of your data when working with a new database for the first time.

5. User-defined functions
02:21 - 03:00
Another way to extend the capabilities of your PostgreSQL database is with user-defined functions. A user-defined function is the PostgeSQL equivalent of a stored procedure where you can bundle several SQL queries and statements together into a single package using the CREATE FUNCTION command. In this example we define the function squared that accepts an integer, i, as an input parameter and returns the square of that parameter as the result. The double dollar sign syntax specifies that the function will be using SQL as the language.

6. User-defined functions in the Sakila database
03:00 - 04:01
In addition to being an excellent sample relational database, the Sakila DVD Rental Database that you've been using as the dataset throughout this course also showcases the power of PostgreSQL extensibility and comes pre-installed with a few examples of custom or user-defined functions for you to explore and experiment with. The get_customer_balance function takes a customer_id and a timestamp as input parameters and will calculate the current balance of a customer based on a customer_id as of the timestamp date. The inventory_held_by_customer function takes an inventory_id as an input parameter and will determine all rows that have a return_date equal to null which means the customer still has the rental. And finally the inventory_in_stock function takes an inventory_id as an input parameter and will determine if a specific inventory_id is in stock.

7. Let's practice!
04:01 - 04:05
Let's take a closer look in the exercises.

### Intro to PostgreSQL extensions

1. Intro to PostreSQL extensions
00:00 - 00:17
You've learned how basic full text search is a better option when searching text data for a string. Next we're going to learn about some common extensions, fuzzystrmatch and pg_trgm, that enhance the full text search capabilities of PostgreSQL.

2. Intro to PostgreSQL extensions
00:17 - 01:00
But first we will learn about the PostgreSQL extension framework in more detail. Most PostgreSQL distributions come bundled with a common set of widely used and supported extensions from the community that can be used by simply enabling them. Here are a few common extensions: PostGIS adds support for allowing location queries to be run in SQL. PostPic allows for image processing within the database. fuzzystrmatch and pg_trgm provide functions that extend full text search capabilities by finding similarities between strings.

3. Querying extension meta data
01:00 - 01:39
To help you discover what extensions are available in your specific PostgreSQL distribution, you can query the pg_available_extensions system view, as shown in this example, to determine a list of extensions that are available to be installed and enabled for use. The results return the name of the first two available extensions. A similar query of the pg_extension system table will tell you which extensions have already been enabled in your database and are currently available for your use. Here we see only one result, the extension plpgsql.

4. Loading extensions into your database
01:39 - 02:21
Any of the extensions that are returned from the pg_available_extensions system view can be loaded into your database and enabled with a simple query using the CREATE EXTENSION command, an example of which is shown here. The IF NOT EXISTS commands can be used to ensure that if the extension has previously been enabled, the query will not generate an error message. Now if we query the pg_extension table again by selecting the extname column for all records, we should see that fuzzystrmatch is now listed with plpgsql.

5. Using fuzzystrmatch or fuzzy searching
02:21 - 03:02
When preforming a full text search based on user input or looking to perform an analysis and comparison of text data in a natural language processing exercise, a function that you will use often is levenshtein from the fuzzystrmatch extension. The levenshtein function calculates the levenshtein distance between two strings which is the number of edits required for the strings to be a perfect match. In this example, you see the distance returned is 2 because in order to convert GUMBO to GAMBOL it would require replacing the U with an A and adding an L to the end of the word or two edits.

6. Compare two strings with pg_trgm
03:02 - 03:58
The pg_trgm extension provides functions and operators to determine the similarity of two strings using trigram matchings. Trigrams are groups of 3 consecutive characters in a string and based on the number of matching trigrams in two strings will provide a measurement of how similar they are. This measurement can be calculated using the similarity function of this extension. The similarity function accepts two parameters; the first being the string you wish to compare and the second being the string you wish to compare against. This function will return a number between 0-1 with zero representing no matching trigrams at all and 1 representing a perfect match. In this example we see that using similarity on GUMBO and GAMBOL returns a value of 0.181818.

7. Let's practice!
03:58 - 04:01
Great job! Let's practice

### Putting it All Together / Wrap Up

1. Putting it All Together
00:00 - 00:04
Let's review what we learned in this course.

2. Functions for manipulating data recap and review
00:04 - 00:58
First you learned about common data types including strings, numerics and arrays. You learned about arrays and their special characteristics and how to use arrays to store lists of data and access and search elements in the list. Next you learned how to manipulate and query date and time objects including how to use the current timestamp in your queries, extract sub fields from existing date and time fields and what to expect when you perform date and time arithmetic. You learned how to manipulate string and text data by transforming case, parsing and truncating text and extracting substrings from larger strings. And finally, you learned about how to extend PostgreSQL capabilities using extensions and explored full text search using the extensions fuzzystrmatch and pg_trgm.

3. Thank you!
00:58 - 01:31
Everything you learned in this course will be foundational in your day to day work with PostgreSQL. The functions you learned will be used again and again as you use SQL to manipulate, extract and transform data from PostgreSQL databases. If you'd like to continue learning about PostgreSQL I encourage you to look at the official PostgreSQL website which contains all official documentation, official source code downloads and installation files as well as a community of users ready to help!


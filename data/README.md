# HOW TO SET UP A SMALL INITIAL MONGODB COLLECTION

What is required? A MongoDB server version 3.4. You can download a MongoDB server at https://www.mongodb.com/download-center?jmp=nav#community.

You must have at least version 3.4 because the document structure uses the new NumberDecimal data format. All the code in the 'ndecimal' directory creates a collection with documents that contain fields in NumberDecimal format. 

Once your server is set up and running, the fun begins. 

If you want to work with fields in NumberDecimal format, please change to the 'ndecimal' directory. If you want to work with fields in NumberLong format, please change to the 'nlong' directory. Once you are in one of these directories, the files shown below can be added in any order:
```
test_add_fizzie
test_add_garbuckle
test_add_smith
```

In Linux or MacOS, you can open a shell promopt and start the mongo shell.

You can add the above files using the mongo shell like this (as an example):

```
mongo < test_add_fizzie
```
This file:

```
test_add_second_ride_smith
```

...can only be added after the member Smith has been initially added to the collection.
This is because the update method is being called, not the insert method. The document 
to be updated must already exist.

##Database Collections

You can create collections with the "miles" and "points" fields which are in either NumberDecimal or NumberLong format. Just use the scripts in the appropriate directories, as explained above.

The collection ride_journal1 contains documents with the "miles" and "points" fields in NumberDecimal format.

The collection ride_journal2 contains documents with the "miles" and "points" fields in NumberLong format.

##NumberLong Format Requires Programming With A Scale Factor
Values inserted for the "miles" and "points" fields for the NumberLong data type are intended (for purposes of this project) to be treated with an implied decimal point of two digits precision. So if you see a raw value such as NumberLong(500), the intent of this project is that the value is actually 5.00, not 500.00. Programming has to be done with a scale factor that gives us 2 decimal places of precision. Please note that the NumberLong data format does not in itself format values with an implied decimal point. Instead, the implied decimal point is applied at the project level: we decide the precision we need, and write scripts containing scale factors appropriate to the decimal precision required.

### Note about the 'miles' and 'points' fields in the document collection.
It was discovered during initial efforts to aggregate the data through Node.js scripts that the mongodb JavaScript driver does not support NumberDecinal format. It was decided to create scripts for setting up test documents that have these fields in NumberLong format. That way, database users can have a choice of which data format they prefer using. For now (January 2017), it appears that NumberLong may be the only viable format for Node developers, until the mongodb javascript driver supports NumberDecimal. The MongoDB Java driver does support NumberDecimal at this writing.
 

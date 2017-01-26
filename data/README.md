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

### Note about the 'miles' and 'points' fields in the document collection.
It was discovered during initial efforts to aggregate the data through Node.js scripts that the mongodb JavaScript driver does not support NumberDecinal format. It was decided to create scripts for setting up test documents that have these fields in NumberLong format. That way, database users can have a choice of which data format they prefer using. For now (January 2017), it appears that NumberLong may be the only viable format for Node developers, until the mongodb javascript driver supports NumberDeciaml. The MongoDB Java driver, however, does support NumberDecimal at this writing.
 
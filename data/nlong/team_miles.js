db.ride_journal2.aggregate(
[
  { $unwind : "$rides" },
  { $group : { _id : "$team", tot_miles : { $sum : "$rides.miles" } } },
  { $sort : { "tot_miles" : -1 } }

]
)
from datetime import timedelta

from sqlalchemy import text
from stravalib import unithelper as uh

from bafs import app, db
from bafs.model import RidePhoto, Ride
from bafs.utils import auth
from flask import Blueprint, jsonify

blueprint = Blueprint('api', __name__)


@blueprint.route("/stats/general")
@auth.crossdomain(origin='*')
def stats_general():
    q = text("""select count(*) as num_contestants from athletes WHERE team_id is not null""")

    indiv_count_res = db.session.execute(q).fetchone()  # @UndefinedVariable
    contestant_count = indiv_count_res['num_contestants']

    q = text("""
                select count(*) as num_rides, coalesce(sum(R.moving_time),0) as moving_time,
                  coalesce(sum(R.distance),0) as distance
                from rides R
                ;
            """)

    all_res = db.session.execute(q).fetchone()  # @UndefinedVariable
    total_miles = int(all_res['distance'])
    total_hours = uh.timedelta_to_seconds(timedelta(seconds=int(all_res['moving_time']))) / 3600
    total_rides = all_res['num_rides']

    q = text("""
                select count(*) as num_rides, coalesce(sum(R.moving_time),0) as moving_time
                from rides R
                join ride_weather W on W.ride_id = R.id
                where W.ride_temp_avg < 32
                ;
            """)

    sub32_res = db.session.execute(q).fetchone()  # @UndefinedVariable
    sub_freezing_hours = uh.timedelta_to_seconds(timedelta(seconds=int(sub32_res['moving_time']))) / 3600

    q = text("""
                select count(*) as num_rides, coalesce(sum(R.moving_time),0) as moving_time
                from rides R
                join ride_weather W on W.ride_id = R.id
                where W.ride_rain = 1
                ;
            """)

    rain_res = db.session.execute(q).fetchone()  # @UndefinedVariable
    rain_hours = uh.timedelta_to_seconds(timedelta(seconds=int(rain_res['moving_time']))) / 3600

    q = text("""
                select count(*) as num_rides, coalesce(sum(R.moving_time),0) as moving_time
                from rides R
                join ride_weather W on W.ride_id = R.id
                where W.ride_snow = 1
                ;
            """)

    snow_res = db.session.execute(q).fetchone()  # @UndefinedVariable
    snow_hours = uh.timedelta_to_seconds(timedelta(seconds=int(snow_res['moving_time']))) / 3600

    return jsonify(
            team_count=len(app.config['BAFS_TEAMS']),
            contestant_count=contestant_count,
            total_rides=total_rides,
            total_hours=total_hours,
            total_miles=total_miles,
            rain_hours=rain_hours,
            snow_hours=snow_hours,
            sub_freezing_hours=sub_freezing_hours)


@blueprint.route("/photos")
@auth.crossdomain(origin='*')
def list_photos():
    photos = db.session.query(RidePhoto).join(Ride).order_by(Ride.start_date.desc())

    results = []
    for p in photos:
        results.append(dict(id=p.id,
                            ref=p.ref,
                            caption=p.caption,
                            uid=p.uid,
                            ride_id=p.ride_id,
                            thumb_url='http://127.0.0.1:5000/photos/{}.jpg'.format(p.uid)
                            # This is temporary until we change how we store these.
                            ))
    return jsonify(dict(result=results, count=len(results)))


@blueprint.route("/leaderboard/team")
@auth.crossdomain(origin='*')
def team_leaderboard():
    """
    Loads the leaderboard data broken down by team.
    """
    q = text("""
             select T.id as team_id, T.name as team_name, sum(DS.points) as total_score,
             sum(DS.distance) as total_distance
             from daily_scores DS
             join teams T on T.id = DS.team_id
             group by T.id, T.name
             order by total_score desc
             ;
             """)

    team_rows = db.session.execute(q).fetchall()  # @UndefinedVariable

    q = text("""
             select A.id as athlete_id, A.team_id, A.display_name as athlete_name,
             sum(DS.points) as total_score, sum(DS.distance) as total_distance,
             count(DS.points) as days_ridden
             from daily_scores DS
             join athletes A on A.id = DS.athlete_id
             group by A.id, A.display_name
             order by total_score desc
             ;
             """)

    team_members = {}
    for indiv_row in db.session.execute(q).fetchall():  # @UndefinedVariable
        team_members.setdefault(indiv_row['team_id'], []).append(indiv_row)

    for team_id in team_members:
        team_members[team_id] = reversed(sorted(team_members[team_id], key=lambda m: m['total_score']))

    rows = []
    for i, res in enumerate(team_rows):
        place = i + 1

        members = [{'athlete_id': member['athlete_id'],
                    'athlete_name': member['athlete_name'],
                    'total_score': member['total_score'],
                    'total_distance': member['total_distance'],
                    'days_ridden': member['days_ridden']}
                   for member in team_members.get(res['team_id'], [])]

        rows.append({
            'team_name': res['team_name'],
            'total_score': res['total_score'],
            'total_distance': res['total_distance'],
            'team_id': res['team_id'],
            'rank': place,
            'team_members': members
        })

    return jsonify(dict(leaderboard=rows))
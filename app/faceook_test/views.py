from facebook import get_user_from_cookie, GraphAPI
from flask import g, render_template, redirect, request, session, url_for, Blueprint
import requests

# Facebook app details
FB_APP_ID = "542788495882311"
FB_APP_NAME = "Clotify 2.0"
FB_APP_SECRET = "b92b489eb0d50433e216947b14fc41e8"

fb_blueprint = Blueprint('fb_blueprint', __name__, template_folder='templates')

@fb_blueprint.route("/post_message", methods=['GET', 'POST'])
def post_message():
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    response = requests.get("https://graph.facebook.com/v3.0/325373841475462",
                             params={'fields':'access_token', 'access_token':'EAAHtqct8OEcBAGdwEnjZCUqaZBKMrBwMdK9UJm1Orq30a1rxSouZCgvl0sOZAsIjNARvCsU2UBXLeWcz3vc7GZBccURIlnEZCT4TzyeWHBXuNFPUFaNAYiZBnj8ZBuwCCRB43fpfwbJA0WufQqpYAzVWGGlAoktucmwNAzzy5QZARNQU1uxPUrkbVA8uI3jX7JKpDEnZA3cH8evgZDZD'},
                             headers=None)
    data = response.json()
    print(data)

    response1 = requests.post("https://graph.facebook.com/v3.0/325373841475462/feed",
                             data={'message':'Test bai', 'access_token':data['access_token']},
                             headers=None)
    data1 = response1.json()
    return redirect(url_for('fb_blueprint.index'))


@fb_blueprint.route("/fb_test", methods=['GET', 'POST'])
def index():
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    get_current_user()
    if g.user:
        return render_template(
            "fb_index.html", app_id=FB_APP_ID, app_name=FB_APP_NAME, user=g.user
        )
    # Otherwise, a user is not logged in.
    return render_template("fb_login.html", app_id=FB_APP_ID, name=FB_APP_NAME)


@fb_blueprint.route("/fb_test/logout", methods=['GET', 'POST'])
def logout():
    get_current_user()
    """Log out the user from the application.

    Log out the user from the application by removing them from the
    session.  Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    session.pop("user", None)
    return redirect(url_for("fb_blueprint.index"))


def get_current_user():
    """Set g.user to the currently logged in user.

    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.  A currently logged in user is
    determined by seeing if it exists in Flask's session dictionary.

    If it is the first time the user is logging into this application it will
    create the user and insert it into the database.  If the user is not logged
    in, None will be set to g.user.
    """

    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    if session.get("user"):
        g.user = session.get("user")
        return

    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(
        cookies=request.cookies, app_id=FB_APP_ID, app_secret=FB_APP_SECRET
    )

    # If there is no result, we assume the user is not logged in.
    if result:
        # Check to see if this user is already in our database.

        # Not an existing user so get info
        graph = GraphAPI(result["access_token"])
        profile = graph.get_object("me")
        if "link" not in profile:
            profile["link"] = ""
        print(profile)
        print(result)

        # Create the user and insert it into the database
        # Add the user to the current session
        session["user"] = dict(
            name=profile["name"],
            profile_url=profile["link"],
            id=str(profile["id"]),
            access_token=result["access_token"],
        )

    # Commit changes to the database and set the user as a global g.user
    g.user = session.get("user", None)

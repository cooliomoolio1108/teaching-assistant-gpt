from flask import Blueprint, redirect, request, url_for, session, render_template, current_app, make_response
from auth.msal_helper import build_msal_app, get_auth_url, create_jwt, upsert_user_from_claims
import uuid
import os
from dotenv import load_dotenv
from database import user_collection

load_dotenv()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return redirect(get_auth_url(str(uuid.uuid4())))

@auth_bp.route("/getAuth")
def authorized():
    result = build_msal_app().acquire_token_by_authorization_code(
        request.args.get("code"),
        scopes=["User.Read"],
        redirect_uri=url_for("auth.authorized", _external=True)
    )
    
    claims = result.get("id_token_claims", {})
    print("CLAIMS: ", claims)
    email = claims.get("preferred_username", "")
    domain = email.split('@')[-1]

    if domain not in {"ntu.edu.sg", "e.ntu.edu.sg"}:
        return render_template("error.html", message="Access denied: NTU emails only", home_url=current_app.config["FRONTEND_URL"])
    
    user = upsert_user_from_claims(user_collection, claims)

    jwt_token = create_jwt(user['email'], user['name'], user['oid'])
    resp = make_response(redirect(os.getenv("STREAMLIT_URL")))
    resp.set_cookie(
        "login_token",
        jwt_token,
        httponly=False,       # Prevent JavaScript access
        secure=True,         # Only send over HTTPS
        samesite="Lax"       # Adjust depending on cross-site needs
    )
    return resp
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("https://login.microsoftonline.com/common/oauth2/v2.0/logout")

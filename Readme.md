# Google oauth2 example with Flask and SQLAlchemy

  Example code for using oauth2 with Flask

## Issues

Flask OAuth has a bug fix that may not yet be on PyPi.  Add the following to requirements.txt and remove Flask-OAuth==0.11:

```text
git+https://github.com/mitsuhiko/flask-oauth
```

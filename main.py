#
# Followed Tech w/ Tim's tutorial on Creating Web Application w/ Flask
# URL: (https://www.youtube.com/watch?v=dam0GPOAvVI&pp=ygUkdGVjaCB3aXRoIHRpbSBweXRob24gd2ViIGFwcGxpY2F0aW9u)
#

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
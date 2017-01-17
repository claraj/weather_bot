import webapp2

main_page_html = '''<DOCTYPE html>
<html>
<head><title>Minneapolis-St. Paul Most Cold?</title></head>
<body><P>Does Minneapolis-St. Paul have the lowest high temperature out of the 80 largest cities in the US?</P>
<P>This Twitter bot will check for you. You can visit it here: <a href="https://twitter.com/mpls_most_cold">Minneapolis Coldest? (@mpls_most_cold)</a> </body>
</html>
'''

class PagesHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write(main_page_html)



app = webapp2.WSGIApplication([
    ('/', PagesHandler)
])

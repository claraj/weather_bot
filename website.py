import webapp2

main_page_html = '''<DOCTYPE html>
<html>
<head><title>Does Minneapolis-St. Paul have the lowest high temperature out of the 100 largest cities in the US??</title></head>
<body><P>Try visiting Twitter? <a href="https://twitter.com/mpls_most_cold">Minneapolis Coldest (@mpls_most_cold)</a> </body>
</html>
'''

class PagesHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write(main_page_html)



app = webapp2.WSGIApplication([
    ('/', PagesHandler)
])

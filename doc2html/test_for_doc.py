import doc
import unittest

class DocTestCase(unittest.TestCase):

    def test_find_classes(self):
        classes = doc.find_classes(doc)
        cls = sorted([(x.__name__, x.__doc__) for x in classes],
                 key=lambda x: x[0])
        res = [('DocContainer',
                'Class-container that renders object with data for html')]
        self.assertEqual(cls, res)
        
    def test_find_func(self):
        func = doc.find_func(doc)
        ff = sorted([(x.__name__, x.__doc__) for x in func],
                      key=lambda x: x[0])
        res = [('find_classes', 'The function that finds classes in module'),
               ('find_func', 'The function that finds functions in module'),
               ('main', None),
               ('parse_docs', 'The function that handles docstring of module')]
        self.assertEqual(ff, res)


    def test_parse_docs(self):
        res = '''<!DOCTYPE html>
<html>
  <head>
    <title>
      Information about doc module
  </title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" media="screen">
  <style type="text/css">
    .container {
      max-width: 800px;
      padding-top: 50px;
    }
    body {
      background-color: #2d5399;
    }
    div{
      background-color: #99accd;
      margin: 10px;
      border-radius: 5px;
    }
    table{
      background-color: #ccd5e6;
      border-radius: 5px;
    }
    .my_col{
      background-color: #ccd5e6;
      border-radius: 5px;
    }
  </style>
  </head>
  <body>
    <div class="container">
      <p>
        <h1>
          Help: doc
      </h1>
    </p>
    
    <p>
      <h2>
        Description
    </h2>
  </p>
  <table class="table table-hover">
    <p class="my_col">
      The program converts pydoc to html.
    </p>
  </table>
  <p>
    <h3>
      Classes
  </h3>
</p>
<table class="table table-hover">
  <thead>
    <tr>
      <th>
        Name
      </th>
      <th>
        Description
      </th>
    </tr>
  </thread>
  
  <tbody>
    
    <tr>
      
      <td>
        DocContainer
      </td>
      <td>
        Class-container that renders object with data for html
      </td>
      
    </tr>
    
  </tbody>
</table>



<p>
  <h3>
    Functions
</h3>
</p>

<table class="table table-hover">
  <thead>
    <tr>
      <th>
        Name
      </th>
      <th>
        Description
      </th>
    </tr>
  </thread>
  
  <tbody>
    
    <tr>
      
      <td>
        find_classes
      </td>
      <td>
        The function that finds classes in module
      </td>
      
    </tr>
    
    <tr>
      
      <td>
        find_func
      </td>
      <td>
        The function that finds functions in module
      </td>
      
    </tr>
    
    <tr>
      
      <td>
        main
      </td>
      <td>
        no information
      </td>
      
    </tr>
    
    <tr>
      
      <td>
        parse_docs
      </td>
      <td>
        The function that handles docstring of module
      </td>
      
    </tr>
    
  </tbody>
</table>
</div>
</body>
</html>'''
        cur_res = doc.parse_docs(doc, 1).__str__()
        self.assertEqual(cur_res, res)

if __name__ == '__main__':
    unittest.main()

# ==================================================================================================
"""TOOLS : a set of handy tools for common data processing tasks"""
# ==================================================================================================
__author__  = "Christophe Schlick"
__version__ = "1.0"
__date__    = "2022-06-01"
# ==================================================================================================
def show(string):
  """split, eval, print a string containing python expressions separated by semi-colons"""
  from inspect import stack; from pprint import pprint
  namespace = stack()[1][0].f_globals # get global namespace from caller
  namespace = dict((k,v) for (k,v) in namespace.items() if k[0] != '_')
  for exp in string.split(';'):
    exp = exp.strip(); head, tail = exp[:1], exp[-1:]
    head, exp = (head, exp[1:]) if head == '*' else ('', exp) 
    tail, exp = (tail, exp[:-1]) if tail == '#' else ('', exp)
    val = eval(exp, namespace) if exp else ''
    if exp: print(head+exp if head else exp, '=\n' if tail else '= ', end='')
    print(*val) if head else pprint(val) if tail else print(val)
# --------------------------------------------------------------------------------------------------
def load(filename, split=True, strip=True, clean=True, comment='#', encoding='utf8'):
  """load content of provided text file and perform split/strip/clean tasks
  - filename:str = path to file on disk
  - split:bool = split file content to return list of lines instead of multi-line string
  - strip:bool = remove boundary whitespaces for each line
  - clean:bool = remove empty lines and comment lines
  - comment:char = prefix char defining comment lines
  - encoding:str = character encoding used for file reading"""
  with open(filename, 'r', encoding=encoding) as file: text = file.read()
  if strip: text = text.strip() # strip whole content
  if not split: return text # return content as a multi-line string
  text = text.split('\n') # split into lines
  if strip: text = [line.strip() for line in text]
  if not clean: return text # return content as a list of lines
  text = [line for line in text if line and line[0] != comment] # clean comments and empty lines
  return text # return content as a list of cleaned lines
# --------------------------------------------------------------------------------------------------
def save(filename, body='', head='', append=False, comment='# ', encoding='utf8'):
  """save string or iterable into provided text file with optional comment header
  Optional keyword arguments :
  - body:str|list|tuple = content for file body (converted into data lines)
  - head:str|list|tuple = content for file head (converted into comment lines)
  - append:bool : append head+body at existing content, instead of overwrite
  - comment:char = prefix char defining comment lines
  - encoding:str = character encoding used for file reading"""
  if head: # process header data
    if not isinstance(head,str): head = '\n'.join(str(line) for line in head)
    head = comment + head.replace('\n','\n'+comment) + '\n' # add comment prefixes
  if body: # process body data
    if not isinstance(body,str): body = '\n'.join(str(line) for line in body)
    if body[-1] != '\n': body += '\n' # add final newline if missing
  mode = 'wa'[append] # select either 'write' or 'append' mode
  with open(filename, mode, encoding=encoding) as file: file.write(head + body)
# --------------------------------------------------------------------------------------------------
def hscroll(activate=True):
  """activate/deactivate horizontal scrolling for wide output (> 120 chars)"""
  from IPython.display import display, HTML
  style = ('pre-wrap','pre')[activate] # select white-space style
  display(HTML("<style>pre {white-space: %s !important}</style>" % style))
# ==================================================================================================

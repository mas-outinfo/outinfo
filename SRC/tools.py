# ==================================================================================================
"""TOOLS : a set of handy tools for common data processing tasks"""
# ==================================================================================================
__author__  = "Christophe Schlick"
__version__ = "1.0"
__date__    = "2022-06-01"
# ==================================================================================================
def show(string):
  """split, eval, print a string containing python expressions separated by semi-colons
  - optional prefix for expression : '*' = unpack items for iterable expression
  - optional suffix for expression : '#' = insert newline before printing expression"""
  from inspect import stack
  namespace = stack()[1][0].f_globals # get global namespace from caller
  namespace = dict((k,v) for (k,v) in namespace.items() if k[0] != '_')
  for exp in string.split(';'):
    exp = exp.strip(); head, tail = exp[:1], exp[-1:]
    head, exp = ('*', exp[1:]) if head == '*' else ('', exp) 
    tail, exp = (' ➤\n', exp[:-1]) if tail == '#' else (' ➤ ', exp)
    if not exp: print(); continue # insert blank line if expression is empty
    val = eval(exp, namespace); print(head + exp + tail, end='')
    print(*val) if head else print(val)
# --------------------------------------------------------------------------------------------------
def view(image, mode=None, clamp=None, file=None):
  """display image with optional image conversion or clamping
  - image:(numpy array or PIL image) = image to display
  - mode:str = PIL image mode = '1'|'L'|'P'|'RGB'|'LA'|'RGBA'
  - clamp:tuple = clamping range for channels = (min, max)
  - file:str = filename for saving on disk"""
  import numpy as np; import PIL.Image as pim
  assert isinstance(image, (np.ndarray, pim.Image)), 'wrong data for image'
  assert isinstance(clamp, (type(None), tuple)), 'wrong range for clamping'
  if isinstance(image, pim.Image): image = np.array(image.convert('RGB') if image.mode == 'P' else image)
  if not clamp: hi = image.max(); clamp = (0, hi if hi else 1)
  lo, hi = clamp; image = (np.clip(image, lo, hi) - lo) / (hi - lo) * 255
  image = pim.fromarray(image.astype('u1'))
  if mode: image = image.convert(mode) # optional: convert image to provided 'mode'
  if file: image.save(file) # optional: save image to provided 'file'
  display(image)
# --------------------------------------------------------------------------------------------------
def inspect(object, detail=0, width=96):
  """show name and docstring for all public members of given object
  - object:Any = object to inspect (usually, module, class or instance)
  - detail:int = level-of-detail for inspection (from 0 to 3)
    0 = show only member names / 1 : show first line of doctrings
    2 = show first block of docstrings / 3 : show whole docstrings
  - width:int = max number of chars per line for output"""
  from inspect import getmembers, getdoc, currentframe; import re
  # ---------------------------------------------------------------------------------------------------
  def getdetail(object, detail, width):
    """return object docstring according to level-of-detail and width"""
    doc = getdoc(object) # get docstring for provided object
    doc = doc.strip() if doc else '<empty docstring>'
    if detail == 3: return doc.replace('\n\n','\n').replace('\n','\n  ') + '\n' # add indentation
    doc = re.sub(r'^[-=]{3,}$','', doc, flags=re.MULTILINE) # remove reStructuredText header marks
    for block in doc.split('\n\n'): # split docstring into blocks (= split on blank lines)
      if '(' not in block.split()[0]: break # discard signature block, if any
    if detail == 2: return block.replace('\n','\n  ') # add indentation
    index = width if '\n' not in block else min(width, block.find('\n')) # get index for truncation
    return block[:index] + ('...' if len(block) > index else '') # add '...' for truncated line
  # ---------------------------------------------------------------------------------------------------
  def fold(names, width):
    """left justify and fold a list of names, according to provided line width"""
    names = [name for name,*info in names] # keep only names
    size = max(map(len, names)) + 2 # get size of longest name (+ padding)
    n = width // size # compute number of names on a single line
    names = [name.ljust(size) for name in names] # left-justify all names
    return '\n'.join(''.join(names[p:p+n]) for p in range(0, len(names), n)) # fold lines
  # ---------------------------------------------------------------------------------------------------
  if hasattr(object, '__name__'): oname = object.__name__
  else: # get object name from caller's namespace when __name__ is not defined
    oname = [key for key,val in currentframe().f_back.f_locals.items() if val is object]
    oname = oname[0] if oname else '<empty name>'
  otype = type(object).__name__; orole = getdetail(object, 2, width-8).strip()
  print('● NAME = ' + oname + ' / TYPE = ' + otype + '\n● ROLE = ' + orole)
  # ---------------------------------------------------------------------------------------------------
  properties, methods, types, modules = [], [], [], []
  for name,member in sorted(getmembers(object)): # loop over object members
    if name[0] == '_': continue # skip all private and special members
    if hasattr(member, '__package__'): # member is an inner module (store name)
      modules.append([name])
    elif hasattr(member, '__base__'): # member is an inner class (store name)
      types.append([name])
    elif hasattr(member, '__call__'): # member is a method or a function (store name and docstring)
      methods.append([name, getdetail(member, detail, width-len(name)-4)])
    else: # member is a property or a constant (store name, type and value)
      mtype = type(member).__name__; pwidth = width-len(name+mtype)-4; pvalue = str(member)
      if pvalue[0] == '<': pvalue = pvalue.split()[0] + '...>' # truncate special values
      else: pvalue = pvalue.replace('\n',' ').strip()
      if len(pvalue) > pwidth: pvalue = pvalue[:pwidth] + '...' + pvalue[-1] # truncate long values
      properties.append([name, mtype, repr(member) if mtype == 'str' else pvalue])
  # ---------------------------------------------------------------------------------------------------
  prompt = f"use 'inspect({oname}.xxx)' to get additional info for each inner"
  groups = [f"MODULES : {prompt} module", f"TYPES : {prompt} type"]
  groups += ['CONSTANTS','FUNCTIONS'] if otype == 'module' else ['PROPERTIES','METHODS']
  if modules: print("\n● %s\n%s" % (groups[0], fold(modules, width)))
  if types: print("\n● %s\n%s" % (groups[1], fold(types, width)))
  if detail: # in detail mode, show name, docstring or type/value for each object member
    properties = [f"{name}:{type} = {value}" for name,type,value in sorted(properties)]
    if properties: print("\n● %s\n%s" % (groups[2], '\n'.join(properties)))
    methods = [f"{name} : {doc}" for name,doc in methods]
    if methods: print("\n● %s\n%s" % (groups[3], '\n'.join(methods)))
  else: # in compact mode, show only name for each object member and align names in columns
    if properties: print("\n● %s\n%s" % (groups[2], fold(properties, width)))
    if methods: print("\n● %s\n%s" % (groups[3], fold(methods, width)))
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

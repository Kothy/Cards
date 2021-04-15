import ctypes


# CONSTATNTS
FILETYPES = [("PNG obrázky", "*.png"), ("JPG obrázky", "*.jpg"), ("JPEG obrázky", "*.jpeg")]
SAVEFILETYPES = [("JSON súbory", "*.json")]
OBJID = 1
IMGREMOVE = False

# SIZES
user32 = ctypes.windll.user32
WWIDTH = user32.GetSystemMetrics(0)
WHEIGHT = user32.GetSystemMetrics(1) - 65

# WWIDTH = 800
# WHEIGHT = 600

TEWIDTH = 100
TEHEIGHT = 100
CWIDTH = WWIDTH - 350
CHEIGHT = WHEIGHT - 100
RBARW = 60
DBARH = 45
DESKTOPWMAX = WWIDTH - 100
DESKTOPHMAX = WHEIGHT - 60
CLICKABLEMAX = 30

# COLORS
PRIMARYCOLOR = '#f8d3ec'
SECONDARYCOLOR = '#c5b6e2'
TERNARYCOLOR = '#d7f4d9'
WHITE = "white"
RED = "red"
BLACK = "black"

QUARTERYCOLOR = "#ffffff"
TEBG = PRIMARYCOLOR
DOWNBARCOLOR = PRIMARYCOLOR  # "#cccccc"
OUTERCANVASBGCOLOR = TERNARYCOLOR  # '#e6e6e6'
DESKTOPBGCOLOR = QUARTERYCOLOR
RBARBG = PRIMARYCOLOR
OBJECTSCALECOLOR = SECONDARYCOLOR

# TEXTS
FONT = "Montserrat"
FONTTEXT = "font"
DOTDOTDOT = "..."
OBJECTINFO = '  Info o objekte: {}  '
OBJECTINFOEMPTY = '  Info o objekte:    '
CHANGEIMAGES = "Zmeniť obrázky"
CHANGEIMAGE = "Zmeniť obrázok"
REMOVEOBJECT = "Odstrániť"
SELECT = "Označiť"
DESELECT = "Odznačiť"
SELECTDESELECT = "Označiť / Odznačiť"
COPY = "Kopírovať"
PASTE = "Vložiť"
CREATEGRID = "Vytvoriť mriežku z tohoto objektu"
CHOOSEIMAGE = "Vyber obrázok"
CHOOSEIMAGES = "Vyber jeden alebo viac obrázkov"
CHOOSECOLOR = "Vyber farbu"
CHANGEFONT = "Zmeniť písmo a jeho štýl"
CHANGEFONTCOLOR = "Zmeniť farbu písma"
CHANGEBGCOLOR = "Zmeniť farbu pozadia"
CHOOSEFONT = "Vyber písmo"
CANVASSIZE = "  Rozmer plochy: {}, {}   "
CURSORPOSEMPTY = '  Pozícia kurzoru: 0, 0   '
CURSORPOSITION = '  Pozícia kurzoru: {}, {}   '
UPSIZE = "Zvačšiť"
DOWNSIZE = "Zmenšiť"
FLIPHORIZONTALLY = "Prevrátiť vodorovne"
FLIPVERTICALLY = "Prevrátiť zvislo"
COPYPASTE = "Kopírovať a vložiť"
SET = "Nastaviť"
AVAILBUTTONS = "Dostupné tlačidlá"
TOOLS = "Nástroje: "
SAVEASEULOHA = "Vyber priečinok a názov pre eÚlohu"
CHOOSEEULOHAJSON = "Vyber súbor s eÚlohou (*.json)"
BACKTOMENU = "Späť do menu"
NEWEULOHA = "Nová eÚloha"
LOADULOHA = "Načítať úlohu"
OPENEULOHA = "Otvoriť eÚlohu"
SAVEEULOHA = "Uložiť ako eÚlohu"
SAVEULOHA = "Uložiť úlohu"
SAVEEZOSIT = "Ulož ako eZošit"
HEIGHT = "Výška"
WIDTH = "Šírka"
ADDSTATIC = "Vložiť statický objekt"
ADDDRAGGABLE = "Vložiť ťahateľný objekt"
ADDCLONABLE = "Vložiť klonovateľný objekt"
ADDCLICKABLE = "Vložiť klikateľný objekt"
ADDTEXT = "Vložiť textový objekt"
SETBGIMG = "Nastaviť obrázok pozadia"
REMOVEBGIMG = "Odstrániť obrázok pozadia"
CHANGEBGIMG = "Zmeniť obrázok pozadia"
SETBGCOLOR = "Nastaviť farbu pozadia"
SETDRAGGABLE = "Nastaviť mód ťahania"
SETCLONABLE = "Nastaviť mód klonovania"
CHANGEORDERIMAGES = "Zmeniť poradie obrázkov"
SUBMIT = "Potvrdiť"
CANCEL = "Zrušiť"
TEXTTYPE = "Text"
DRAGGABLE = "Ťahateľný"
CLICKABLE = "Klikateľný"
STATIC = "Statický"
CLONABLE = "Klonovateľný"
HOME = "Home"
ROTATE = "Otočiť o 90 stupňov"
CREATEHOME = "Vytvoriť domovskú polohu"
ERROR = "Chyba"
WRITE = "w"
READ = "r"
CENTER = "c"
NW = "nw"
ALL = "all"
JSONPOSTFIX = ".json"
INDEXONE = "1.0"
SAVE = "Uložiť"
WANTSAVE = "Želáte si uložiť aktuálnu úlohu ?"
HIDDEN = "hidden"
NORMAL = "normal"
LIMITEXCEEDED = "Maximálny počet obrázkov je 30."
EMPTYSTRING = ""
DEFAULTFONT = "Montserrat"
COLOR = "color"
SIZE = "size"
SLANT = "slant"
FAMILY = "family"
UNDERLINE = "underline"
OVERSTRIKE = "overstrike"
WEIGHT = "weight"
SYSTEMHIGHLIGHT = "SystemHighlight"
ROMAN = "roman"
SHOWHOMES = "Zobraziť domovské miesta"
HIDEHOMES = "Skryť domovské miesta"
BOLD = "bold"
W = "w"
DISABLED = "disabled"
ROWNUM = "Počet riadkov"
COLNUM = "Počet stĺpcov"
GRIDCOLOR = "Farba mriežky"
GRIDLINE = "Čiara mriežky"
SPINSTYLE = "Klaudia.TSpinbox"

# JSON keys
JSONX = "x"
JSONY = "y"
JSONWIDTH = "width"
JSONHEIGHT= "height"
JSONTYPE = "type"
JSONIMAGE = "image"
JSONIMAGES = "images"
JSONOBJECTS = "objects"
JSONFONTCOLOR = "fontcolor"
JSONFONTSIZE = "fontsize"
JSONFONT = "fontfamily"
JSONFONTUNDER = "fontunderline"
JSONFONTSTRIKE = "fontoverstrike"
JSONFONTWEIGHT = "fontweight"
JSONFONTSLANT = "fontslant"
JSONFONTFAMILY = "fontfamily"
JSONBGCOLOR = "bgcolor"
JSONTEXT = "text"
JSONBGIMAGE = "bgimage"
JSONAVILBUTT = "availbuttons"
JSONGRID = "Grid"
JSONCOLOR = "color"
GRIDOBJECTS = "grids"
HOMEOBJECTS = "homeobjects"
JSONHOMESVIS = "homesvisible"


# Binds
BINDMOUSEWHEEL = "<MouseWheel>"
BINDDELETE = "<Delete>"
BINDLEAVE = "<Leave>"
BINDENTER = "<Enter>"
BINDMOTION = "<Motion>"
BINDRIGHTBUTT = "<Button-3>"
BINDRIGHTMOTION = "<B1-Motion>"
BINDLEFTBUTT = "<Button-1>"
BINDLEFTRELEASE = "<ButtonRelease-1>"
BINDDOUBLELEFT = "<Double-Button-1>"

# Cursors
HORIZARROW = "sb_h_double_arrow"
VERTICARROW = "sb_v_double_arrow"

# Styles
SUBMITSTYLE = "Submit.TButton"
MYKCHECKSTYLE = "MyK.TCheckbutton"

types = dict()
types[TEXTTYPE] = TEXTTYPE
types[DRAGGABLE] = "Draggable"
types[CLICKABLE] = "Clickable"
types[CLONABLE] = "Clonable"
types[STATIC] = "Static"

types["Draggable"] = DRAGGABLE
types["Clickable"] = CLICKABLE
types["Static"] = STATIC
types["Clonable"] = CLONABLE
types["Home"] = "Home"

# ICONS
ICOHOME = "images/buttons/home.png"
ICONEWTASK = "images/buttons/new.png"
ICOOPENTASK = "images/buttons/openTask.png"
ICOSAVEASULOHA = "images/buttons/saveAsTask.png"
ICOSAVEASZOSIT = "images/buttons/saveAsBook.png"
ICOUPSIZE = "images/buttons/enlarge.png"
ICODOWNSIZE = "images/buttons/shrink.png"
ICOFLIPH = "images/buttons/flipHorizontal.png"
ICOFLIPV = "images/buttons/flipVertical.png"
ICOCOPY = "images/buttons/copy.png"
ICOPASTE = "images/buttons/paste.png"
ICOREMOVE = "images/buttons/delete.png"
ICOBUTTONPRIMARY = "images/buttons/button6.png"
ICOBUTTONSECONDARY = "images/buttons/button7.png"
ICOBUTTONTERNARY = "images/buttons/button8.png"

# IMAGES
IMAGETRANSPARENT = "images/transparentBg.png"

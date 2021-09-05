import re
import fontforge as ff
from glob import glob

class TTFTask:
  def __init__(self, font, variant, ui) -> None:
    self.font = font
    for locale, name, value in font.sfnt_names:
      if name == "SubFamily":
        self.variant = value
        break
    self.variant = subfamily
    self.ui = ui

  def get_subfamily(self):
    return None

  def edit(self):
    enusr = "Microsoft YaHei"
    if self.ui:
      enusr = "Microsoft YaHei UI"
    enus = enusr + " " + self.variant
    zhcnr = "微软雅黑"
    if self.ui:
      zhcnr = "微软雅黑 UI"
    zhcn = zhcnr + " " + self.variant
    # self.font.fullname = enus
    self.font.fontname = enus.replace(" ", "-")
    self.font.fullname = enus
    self.font.familyname = enusr
    print(self.font.fontname)
    print(self.font.fullname)
    print(self.font.familyname)
    self.font.appendSFNTName("English (US)", "Family", enusr)
    self.font.appendSFNTName("English (US)", "UniqueID", enus)
    self.font.appendSFNTName("English (US)", "Fullname", enus)
    self.font.appendSFNTName("English (US)", "Preferred Styles", self.variant)
    self.font.appendSFNTName("Chinese (PRC)", "Family", zhcnr)
    self.font.appendSFNTName("Chinese (PRC)", "UniqueID", zhcn + " " + self.variant.strip())
    self.font.appendSFNTName("Chinese (PRC)", "Fullname", zhcn)
    self.font.appendSFNTName("Chinese (PRC)", "Preferred Family", zhcn)
    for (lang, key, field) in self.font.sfnt_names:
      print(lang, '%s=%s'%(key, field))
    # print(self.font.sfnt_names)

class TTCFile:
  def __init__(self, file, variant):
    self.file = file
    self.variant = variant
    self.output = transformVariant(variant)

  def openTTF(self, isui):
    target = "Sarasa Gothic SC"
    if isui:
      target = "Sarasa UI SC"
    font = ff.open('%s(%s%s)'%(self.file, target, self.variant))
    return TTFTask(font, self.variant, isui)

  def build(self):
    ttf = self.openTTF(False)
    ttf.edit()
    ttfui = self.openTTF(True)
    ttfui.edit()
    ttf.font.generateTtc("out/%s"%self.output, ttfui.font, ttcflags = ("merge"), layer = 1)
    ttf.font.close()
    ttfui.font.close()
  
  def __str__(self) -> str:
    return 'TTCFile(%s, %s) -> %s'%(self.file, self.variant, self.output)

def listTtc(pattern):
  for ttc in glob(pattern):
    for face in ff.fontsInFile(ttc):
      if m := re.match(r"Sarasa Gothic SC(.*)?", face):
        yield TTCFile(ttc, m.group(1))

def transformVariant(input):
  ret = "msyh"
  if "Bold" in input:
    ret += "bd"
  if "Semibold" in input:
    ret += "sb"
  if "Light" in input:
    ret += "l"
  if "Xlight" in input:
    ret += "xl"
  if "Italic" in input:
    ret += "i"
  return ret + ".ttc"

for ttc in listTtc("data/*.ttc"):
  print(ttc)
  ttc.build()
from PIL import Image

class PatternManager:
  def __init__(self):
    self.cache = {}

  def clearCache(self):
    self.cache = {}

  # static method
  # this math is pretty arbitrary but we decompose it in case it needs
  # to be tweaked or inspected later
  def brtFromPixel(pixel):
    # average the RGB components; alpha not supported at this time
    colorValue = sum(pixel)/len(pixel)
    # invert, because black = brightest
    # scale from 0-255 to 0-15
    return int((255-colorValue)*15 / 255)

  # static method
  def patFromImage(icon):
    pattern = []
    img = Image.open('icons/'+icon)
    pixels = img.load()

    for y in range(0, img.size[1]):
      pattern.append([])
      for x in range(0, img.size[0]):
        pattern[y].append(PatternManager.brtFromPixel(pixels[x, y]))

    img.close()
    return pattern

  # static method
  # assume same number of rows
  # merge in place and return pat1
  def mergeHorizontal(pat1, pat2):
    merged = []
    for row in range(0, len(pat1)):
      merged.append(pat1[row] + pat2[row]) # python makes merging trivially easy
    return merged

  def getPattern(self, icon):
    if icon not in self.cache:
      self.cache[icon] = PatternManager.patFromImage(icon)

    return self.cache[icon] 

  # static method
  def getPatterns(self, patterns):
    if type(patterns) != list:
      return self.getPattern(patterns)

    if len(patterns) < 1:
      return None

    mosaic = self.getPattern(patterns[0])
    for i in range(1, len(patterns)):
      mosaic = PatternManager.mergeHorizontal(mosaic, self.getPattern(patterns[i]))

    return mosaic

COLS_PER_BYTE = 2

def compress(pattern):
  message = []
  char = 0
  for row in pattern:
    for c in range(0, len(row)):
      offset = (c % COLS_PER_BYTE)
      char |= row[c] << int(8*offset/COLS_PER_BYTE)
      if offset == COLS_PER_BYTE - 1:
        message.append(char)
        char = 0
  return bytes(message)

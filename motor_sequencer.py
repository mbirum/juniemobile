forward_sequence = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

def forward():
  return forward_sequence

def backward():
  backward_sequence = []
  last_index = len(forward_sequence) - 1
  for i in range(len(forward_sequence)):
    index = last_index - i
    backward_sequence.append(forward_sequence[index])
  return backward_sequence
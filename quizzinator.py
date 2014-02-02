from sys import argv

def characterToValueMap(lineArr):
  char_map = {}
  desc_map = {}
  img_map = {}
  curr_char = 0
  next_desc = False
  next_image = False
  for line in lineArr:
    if 'class="quiz_result has_result_image"' in line:
      line = line.strip()
      name_index = line.index('rel:name')
      name = line[name_index + 10:-1]
      char_map[curr_char] = name
      next_desc = True
    elif next_desc:
      line = line.strip()
      desc = line[17:-2]
      desc_map[curr_char] = desc
      next_desc = False
      next_image = True
    elif next_image and 'img class="result_img' in line:
      line = line.strip()
      src_index = line.index('src')
      img_src = line[src_index + 5:-3]
      img_map[curr_char] = img_src
      next_image = False
      curr_char += 1


  return char_map, desc_map, img_map

def characterToAnswersMap(lineArr):
  ans_map = {}
  q_to_img_map = {}
  step = -1
  curr_q = -1
  curr_char = -1
  for line in lineArr:
    if 'div class="quiz_question_header"' in line:
      step = 0
      curr_q += 1
    if step == 0 and 'img class="quiz_img largeImg"' in line:
      line = line.strip()
      src_index = line.index('src')
      q_src = line[src_index + 5:-1]
      q_to_img_map[curr_q] = q_src
      step = 1
    if step == 1 and 'li class="quiz_answer' in line:
      line = line.strip()
      person_index = line.index('rel:personality_index=')
      add = len('rel:personality_index=')
      curr_char_line = line[person_index + add:-1]
      curr_char = int(curr_char_line.strip('"'))
      if not curr_char in ans_map:
        ans_map[curr_char] = {}
      step = 2
    if step == 2 and 'img src=' in line:
      line = line.strip()
      src_index = line.index('src=')
      img = line[src_index + 5:-3]
      ans_map[curr_char][curr_q] = img
      step = 1

  return ans_map, q_to_img_map


f = open(argv[1])
descMap = {}
char2Q2AnswerMap = {}

currQ = 0
currAns = 0
# 0 -> next is question,
# 1 -> next is question image
# 2 -> next is answer, w/ personality_index
# 3 -> next is answer image
# 4 -> now looking at results
state = 0

lineArr = []
for line in f:
  lineArr.append(line)

char_map, desc_map, char_to_image = characterToValueMap(lineArr)
ans_map, q_to_img_map = characterToAnswersMap(lineArr)

print '<html><body>'
print ('<p>Source for content (pulling a BuzzFeed here): ' +
'<a href="http://www.buzzfeed.com/marietelling/which-harry-potter-character-are-you">' +
'Buzzfeed.com' +
'</a></p>')
for char in char_map:
  print '<h2>'
  print char_map[char] + '<br>'
  print '<img src="' + char_to_image[char] + '"/>'
  print '</h2>'
  print '<p>'
  print desc_map[char]
  print '</p>'
  for q in ans_map[char]:
    q_tag = '<img src="' + q_to_img_map[q] + '"/>'
    ans_tag = '<img src="' + ans_map[char][q] + '"/>'
    print '<p>'
    print q_tag
    print ans_tag
    print '</p>'

print '</body></html>'



